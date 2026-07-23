import asyncio
import logging
import uuid
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MockAgent:
    def __init__(self, name: str, signal_type: str, target_url: str = "http://localhost:8000/api/v1/signals/ingest"):
        self.name = name
        self.signal_type = signal_type
        self.target_url = target_url
        self.is_running = False

    async def run_cycle(self):
        logger.info(f"Starting {self.name} Agent cycle...")
        # Simulate finding a lead
        await asyncio.sleep(2)
        logger.info(f"{self.name} Agent completed cycle. (Demo mode)")

    async def start(self):
        self.is_running = True
        while self.is_running:
            await self.run_cycle()
            await asyncio.sleep(120)

    def stop(self):
        self.is_running = False

class GithubAgent(MockAgent):
    def __init__(self):
        super().__init__("GitHub", "competitor_intent")

class LinkedinAgent(MockAgent):
    def __init__(self):
        super().__init__("LinkedIn", "job_change")

class XAgent(MockAgent):
    def __init__(self):
        super().__init__("X/Twitter", "topic_intent")
