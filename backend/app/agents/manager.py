import asyncio
import logging
from typing import Dict, Any

from app.agents.reddit import RedditAgent
from app.agents.mocks import GithubAgent, LinkedinAgent, XAgent

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self):
        self.agents = {
            "reddit": RedditAgent(),
            "github": GithubAgent(),
            "linkedin": LinkedinAgent(),
            "x": XAgent()
        }
        self.tasks = {}

    def start_agent(self, name: str):
        if name in self.agents and name not in self.tasks:
            agent = self.agents[name]
            self.tasks[name] = asyncio.create_task(agent.start())
            logger.info(f"Started {name} agent.")

    def stop_agent(self, name: str):
        if name in self.agents and name in self.tasks:
            self.agents[name].stop()
            task = self.tasks.pop(name)
            task.cancel()
            logger.info(f"Stopped {name} agent.")

    def get_status(self) -> Dict[str, bool]:
        return {name: (name in self.tasks) for name in self.agents}

agent_manager = AgentManager()
