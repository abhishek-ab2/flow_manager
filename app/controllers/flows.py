from fastapi import APIRouter, HTTPException

from app.models.flow import FlowPayload
from app.models.run import StartResponse
from app.repositories.flow import FlowRepository, TaskRegistryRepo
from app.services.flow_manager import FLOW_MANAGER

router = APIRouter(prefix="/flows", tags=["flows"])

@router.post('', status_code=201)
def create_flow(payload: FlowPayload):
    flow = payload.flow
    # Ideally we should have a validation layer for these validations
    # validate task names exist in registry
    registry = TaskRegistryRepo.get_all_tasks()
    valid_names = {r['task_name'] for r in registry}
    for t in flow.tasks:
        if t.name not in valid_names:
            raise HTTPException(status_code=400, detail=f"task {t['name']} not registered")
    fid = FlowRepository.create_flow(flow)
    return {"flow_id": fid}


@router.get('', status_code=200)
def list_flows():
    return FlowRepository.list_flows()

@router.get('/{flow_id}')
def get_flow(flow_id: str):
    f = FlowRepository.get_flow(flow_id)
    if not f:
        raise HTTPException(status_code=404, detail='flow not found')
    return f

@router.post('/{flow_id}/start', response_model=StartResponse)
async def start_flow(flow_id: str):
    # ensure exists
    if not FlowRepository.get_flow(flow_id):
        raise HTTPException(status_code=404, detail='flow not found')
    run_id = await FLOW_MANAGER.start_flow(flow_id)
    return {"run_id": run_id}

@router.get('/{flow_id}/runs')
def list_runs(flow_id: str):
    return FlowRepository.list_runs(flow_id)
