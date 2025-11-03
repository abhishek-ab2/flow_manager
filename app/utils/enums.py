from enum import Enum

class TaskOutcome(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    END = "end"


class FlowRunStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
