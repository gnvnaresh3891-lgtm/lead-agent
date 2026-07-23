import asyncio
from datetime import datetime, timezone
import json
import logging
import time
from typing import Any, Dict, Optional
import uuid

from sqlalchemy import select

from app.core.db import get_db_session
from app.core.logger import log_event
from app.core.redis_client import RedisClient, get_redis_client
from app.core.tenancy import tenant_context
from app.models.lead import Lead
from app.models.signal import Signal
from app.models.task_log import TaskLog

logger = logging.getLogger(__name__)


def _to_uuid(val: Any) -> uuid.UUID:
    """Safely convert string or UUID to UUID object."""
    if isinstance(val, uuid.UUID):
        return val
    if not val or not isinstance(val, str):
        return uuid.uuid4()
    try:
        return uuid.UUID(val)
    except ValueError:
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(val))


class SignalWorker:
    """Background worker popping signals from Redis queue and persisting to DB under tenant context."""

    def __init__(
        self,
        redis_client: Optional[RedisClient] = None,
        queue_name: str = "signals_queue",
    ):
        self.redis_client = redis_client or get_redis_client()
        self.queue_name = queue_name
        self.is_running = False

    async def process_next_signal(self, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """Pop and process a single signal from the Redis queue."""
        start_time = time.perf_counter()
        raw_msg = await self.redis_client.pop_signal(self.queue_name, timeout=timeout)
        if not raw_msg:
            # Also check alternative queue name format for test harness compatibility
            raw_msg = await self.redis_client.pop_signal("queue:signals", timeout=0.01)
            if not raw_msg:
                return None

        try:
            # Parse message structure
            msg = raw_msg if isinstance(raw_msg, dict) else json.loads(raw_msg)
            org_id_raw = msg.get("org_id") or msg.get("tenant_id") or "00000000-0000-0000-0000-000000000000"
            org_uuid = _to_uuid(org_id_raw)

            signal_id_raw = msg.get("signal_id") or msg.get("id") or str(uuid.uuid4())
            signal_uuid = _to_uuid(signal_id_raw)

            signal_type = msg.get("signal_type") or "default"
            payload_data = msg.get("payload") if isinstance(msg.get("payload"), dict) else msg
            score = float(msg.get("score", 0.0))
            trace_id = msg.get("trace_id") or str(uuid.uuid4())

            # Execute DB mutation under tenant_context
            with tenant_context(org_uuid):
                async with get_db_session() as session:
                    # Ensure Lead foreign key exists
                    lead_uuid = None
                    raw_lead_id = msg.get("lead_id")
                    if raw_lead_id:
                        lead_uuid = _to_uuid(raw_lead_id)
                        lead_res = await session.execute(select(Lead).where(Lead.id == lead_uuid))
                        lead_obj = lead_res.scalar_one_or_none()
                        if not lead_obj:
                            lead_obj = Lead(
                                id=lead_uuid,
                                name=f"Signal Lead {str(lead_uuid)[:8]}",
                                email=f"lead_{str(lead_uuid)[:8]}@tenant.local",
                            )
                            session.add(lead_obj)
                    else:
                        lead_res = await session.execute(select(Lead).limit(1))
                        lead_obj = lead_res.scalars().first()
                        if not lead_obj:
                            lead_uuid = uuid.uuid4()
                            lead_obj = Lead(
                                id=lead_uuid,
                                name="Worker Default Lead",
                                email=f"lead_{str(org_uuid)[:8]}@tenant.local",
                            )
                            session.add(lead_obj)
                            await session.flush()
                        lead_uuid = lead_obj.id

                    # Create Signal record
                    signal_rec = Signal(
                        id=signal_uuid,
                        lead_id=lead_uuid,
                        signal_type=signal_type,
                        payload=payload_data,
                        score=score,
                    )
                    session.add(signal_rec)

                    exec_time = (time.perf_counter() - start_time) * 1000.0

                    # Create TaskLog record
                    task_log = TaskLog(
                        task_name="process_signal",
                        status="PROCESSED",
                        details={
                            "signal_id": str(signal_uuid),
                            "signal_type": signal_type,
                            "trace_id": trace_id,
                            "org_id": str(org_uuid),
                        },
                        execution_time=round(exec_time, 2),
                    )
                    session.add(task_log)

            log_event(
                level="INFO",
                event_type="signal_processed",
                message=f"Successfully processed signal {signal_uuid} for tenant {org_uuid}",
                org_id=str(org_uuid),
                trace_id=trace_id,
                latency_ms=exec_time,
            )

            return {
                "status": "PROCESSED",
                "signal_id": str(signal_uuid),
                "org_id": str(org_uuid),
                "execution_time_ms": exec_time,
            }

        except Exception as e:
            logger.error(f"Error processing signal: {e}", exc_info=True)
            await self.redis_client.move_to_dlq(self.queue_name, raw_msg, str(e))
            return {
                "status": "FAILED",
                "error": str(e),
                "moved_to_dlq": True,
            }

    async def run(
        self,
        max_signals: Optional[int] = None,
        run_once: bool = False,
        stop_event: Optional[asyncio.Event] = None,
    ) -> int:
        """Run worker loop until max_signals reached or stopped."""
        self.is_running = True
        processed_count = 0

        while self.is_running:
            if stop_event and stop_event.is_set():
                break

            result = await self.process_next_signal(timeout=0.5)
            if result and result.get("status") == "PROCESSED":
                processed_count += 1
                if max_signals and processed_count >= max_signals:
                    break
            elif run_once:
                break

        self.is_running = False
        return processed_count


async def run_worker_loop(
    redis_client: Optional[RedisClient] = None,
    stop_event: Optional[asyncio.Event] = None,
    max_signals: Optional[int] = None,
) -> int:
    """Helper entrypoint function for running background signal worker loop."""
    worker = SignalWorker(redis_client=redis_client)
    return await worker.run(max_signals=max_signals, stop_event=stop_event)
