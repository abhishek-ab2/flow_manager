from fastapi import APIRouter

from app.repositories.flow import TaskRegistryRepo

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
def list_tasks():
    tasks = TaskRegistryRepo.get_all_tasks()
    print(tasks)
    return [task['task_name'] for task in tasks]
