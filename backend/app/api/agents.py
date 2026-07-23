from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.agents.manager import agent_manager

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

class AgentStatus(BaseModel):
    status: str

@router.get("/")
def get_agents_status() -> Dict[str, bool]:
    return agent_manager.get_status()

@router.post("/{agent_name}/start")
def start_agent(agent_name: str):
    if agent_name not in agent_manager.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent_manager.start_agent(agent_name)
    return {"status": "started", "agent": agent_name}

@router.post("/{agent_name}/stop")
def stop_agent(agent_name: str):
    if agent_name not in agent_manager.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent_manager.stop_agent(agent_name)
    return {"status": "stopped", "agent": agent_name}
