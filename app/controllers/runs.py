import json

from fastapi import APIRouter, HTTPException

from app.repositories.flow import FlowRepository
from app.services.flow_manager import FLOW_MANAGER

router = APIRouter(prefix="/runs", tags=["runs"])

@router.get('/{run_id}')
def get_run(run_id: str):
    r = FlowRepository.get_run(run_id)
    if not r:
        raise HTTPException(status_code=404, detail='run not found')
    flow, tasks = r
    return {**flow, "tasks": tasks}

@router.post('/{run_id}/stop')
async def stop_run(run_id: str):
    await FLOW_MANAGER.stop_run(run_id)
    return {"run_id": run_id, "stopped": True}
