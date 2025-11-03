from app.repositories.flow import TaskRegistryRepo

class TaskRepo:
    @staticmethod
    def get_impl(task_name: str) -> str | None:
        return TaskRegistryRepo.get_impl_for(task_name)

    @staticmethod
    def load_all() -> dict[str, str]:
        rows = TaskRegistryRepo.get_all_tasks()
        return {r['task_name']: r['impl_path'] for r in rows}
