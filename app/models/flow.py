from pydantic import BaseModel
from typing import Any

from app.utils.enums import TaskOutcome


class TaskPayload(BaseModel):
    name: str
    description: str

class ConditionPayload(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: TaskOutcome
    target_task_success: str
    target_task_failure: str

class Flow(BaseModel):
    name: str
    start_task: str
    tasks: list[TaskPayload]
    id: str
    conditions: list[ConditionPayload]

class FlowPayload(BaseModel):
    flow: Flow
