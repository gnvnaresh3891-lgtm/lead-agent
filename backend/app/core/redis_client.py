import asyncio
import collections
from datetime import datetime, timezone
import json
import logging
from typing import Any, Dict, List, Optional, Set, Union

import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis Client wrapper with in-memory fallback queue for local development and testing."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis: Optional[aioredis.Redis] = None
        self.is_fallback: bool = False

        # In-memory fallback structures
        self._fallback_queues: Dict[str, collections.deque] = collections.defaultdict(collections.deque)
        self._fallback_sets: Dict[str, Set[str]] = collections.defaultdict(set)
        self._pending_unacked: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def connect(self) -> bool:
        """Connect to Redis server or fall back to in-memory queue structure."""
        try:
            client = aioredis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=1.0,
                socket_timeout=1.0,
            )
            await client.ping()
            self._redis = client
            self.is_fallback = False
            logger.info(f"Successfully connected to Redis at {self.redis_url}")
            return True
        except Exception as e:
            logger.warning(
                f"Redis server connection failed ({e}). Enabling in-memory async fallback queue."
            )
            self._redis = None
            self.is_fallback = True
            return True

    async def disconnect(self) -> None:
        """Close Redis connection gracefully."""
        if self._redis is not None:
            try:
                await self._redis.aclose()
            except Exception as e:
                logger.warning(f"Error disconnecting from Redis: {e}")
            finally:
                self._redis = None

    async def push_signal(self, queue_name: str, payload: Union[Dict[str, Any], str, List[Any]]) -> int:
        """Push a signal payload into the queue (LPUSH)."""
        if not self.is_fallback and self._redis is not None:
            try:
                data_str = payload if isinstance(payload, str) else json.dumps(payload)
                res = await self._redis.lpush(queue_name, data_str)
                return int(res)
            except Exception as e:
                logger.warning(f"Redis LPUSH error ({e}), switching to fallback queue.")
                self.is_fallback = True

        async with self._lock:
            self._fallback_queues[queue_name].appendleft(payload)
            return len(self._fallback_queues[queue_name])

    async def pop_signal(self, queue_name: str, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """Pop a signal from the queue (RPOP / BLPOP). Returns parsed dictionary or None."""
        if not self.is_fallback and self._redis is not None:
            try:
                res = await self._redis.blpop(queue_name, timeout=max(1, int(timeout)))
                if res:
                    _, raw_data = res
                    if isinstance(raw_data, str):
                        try:
                            return json.loads(raw_data)
                        except json.JSONDecodeError:
                            return {"raw_payload": raw_data}
                    elif isinstance(raw_data, dict):
                        return raw_data
                return None
            except Exception as e:
                logger.warning(f"Redis BLPOP error ({e}), switching to fallback queue.")
                self.is_fallback = True

        start_time = asyncio.get_event_loop().time()
        while True:
            async with self._lock:
                q = self._fallback_queues[queue_name]
                if q:
                    item = q.pop()
                    if isinstance(item, str):
                        try:
                            return json.loads(item)
                        except json.JSONDecodeError:
                            return {"raw_payload": item}
                    elif isinstance(item, dict):
                        return item
                    return {"payload": item}

            if timeout <= 0 or (asyncio.get_event_loop().time() - start_time) >= timeout:
                return None
            await asyncio.sleep(0.01)

    async def get_queue_len(self, queue_name: str) -> int:
        """Get the current length of specified queue."""
        if not self.is_fallback and self._redis is not None:
            try:
                res = await self._redis.llen(queue_name)
                return int(res)
            except Exception as e:
                logger.warning(f"Redis LLEN error ({e}), returning fallback length.")
                self.is_fallback = True

        async with self._lock:
            return len(self._fallback_queues[queue_name])

    async def sadd(self, set_name: str, member: str) -> int:
        """Add member to set. Returns 1 if member added, 0 if already present."""
        if not self.is_fallback and self._redis is not None:
            try:
                res = await self._redis.sadd(set_name, member)
                return int(res)
            except Exception as e:
                logger.warning(f"Redis SADD error ({e}), using fallback set.")
                self.is_fallback = True

        async with self._lock:
            s = self._fallback_sets[set_name]
            if member in s:
                return 0
            s.add(member)
            return 1

    async def sismember(self, set_name: str, member: str) -> bool:
        """Check if member is in set."""
        if not self.is_fallback and self._redis is not None:
            try:
                res = await self._redis.sismember(set_name, member)
                return bool(res)
            except Exception as e:
                logger.warning(f"Redis SISMEMBER error ({e}), using fallback set.")
                self.is_fallback = True

        async with self._lock:
            return member in self._fallback_sets[set_name]

    async def move_to_dlq(
        self, queue_name: str, payload: Union[Dict[str, Any], str, List[Any]], error_reason: str
    ) -> None:
        """Move unprocessable or failed payload to Dead Letter Queue (DLQ)."""
        dlq_item = {
            "payload": payload,
            "error_reason": error_reason,
            "moved_at": datetime.now(timezone.utc).isoformat(),
            "original_queue": queue_name,
        }
        dlq_name = f"dlq:{queue_name}" if not queue_name.startswith("dlq:") else queue_name
        await self.push_signal(dlq_name, dlq_item)
        await self.push_signal("dlq:signals", dlq_item)

    async def clear(self) -> None:
        """Clear in-memory queues and sets (useful for testing)."""
        async with self._lock:
            self._fallback_queues.clear()
            self._fallback_sets.clear()
            self._pending_unacked.clear()
        if not self.is_fallback and self._redis is not None:
            try:
                await self._redis.flushdb()
            except Exception as e:
                logger.warning(f"Error flushing Redis DB: {e}")


# Global default Redis client instance
redis_client = RedisClient()


def get_redis_client() -> RedisClient:
    """Dependency helper to return the global RedisClient instance."""
    return redis_client
