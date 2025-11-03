import asyncio
import importlib
import uuid
from typing import Any

from app.db import db_session
from app.db.run import TaskRun
from app.repositories.flow import FlowRepository, TaskRegistryRepo
from app.utils.enums import TaskOutcome, FlowRunStatus

class FlowManager:
    def __init__(self):
        # Storing the tasks and their status in memory, ideally could use an in memory db like redis.
        self.running_tasks: dict[str, asyncio.Task] = {}
        self.cancellation_events: dict[str, asyncio.Event] = {}
        # cache registry: {task_name: impl_path}
        self.task_impl_cache: dict[str, str] = {r['task_name']: r['impl_path'] for r in TaskRegistryRepo.get_all_tasks()}

    def _load_impl(self, task_name: str) -> str | None:
        # prefer cache
        if task_name in self.task_impl_cache:
            return self.task_impl_cache[task_name]
        impl = TaskRegistryRepo.get_impl_for(task_name)
        if impl:
            self.task_impl_cache[task_name] = impl
        return impl

    @staticmethod
    def _instantiate_task(impl_path: str):
        module_name, class_name = impl_path.split(":")
        module = importlib.import_module(module_name)
        cls = getattr(module, class_name)
        return cls()

    async def start_flow(self, flow_id: str) -> str:
        run_id = str(uuid.uuid4())
        FlowRepository.create_run(run_id, flow_id, FlowRunStatus.PENDING.value)
        cancel_event = asyncio.Event()
        self.cancellation_events[run_id] = cancel_event
        task = asyncio.create_task(self._run_flow(flow_id, run_id, cancel_event))
        self.running_tasks[run_id] = task
        return run_id

    async def stop_run(self, run_id: str):
        ev = self.cancellation_events.get(run_id)
        task = self.running_tasks.get(run_id)
        if ev:
            ev.set()
        if task:
            task.cancel()
        FlowRepository.update_run_status(run_id, FlowRunStatus.CANCELLED)

    async def _run_flow(self, flow_id: str, run_id: str, cancel_event: asyncio.Event):
        FlowRepository.update_run_status(run_id, FlowRunStatus.RUNNING)
        try:
            flow = FlowRepository.get_flow(flow_id)
            if not flow:
                FlowRepository.update_run_status(run_id, FlowRunStatus.FAILED)
                return

            tasks_by_name = {t['name']: t for t in flow.get('tasks', [])}
            conditions = flow.get('conditions', [])
            current = flow.get('start_task')
            prev_output = None

            while current and current != TaskOutcome.END.value:
                if cancel_event.is_set():
                    raise asyncio.CancelledError()

                if current not in tasks_by_name:
                    FlowRepository.store_task_run(run_id, current, TaskOutcome.FAILURE.value, None, "task not defined")
                    break

                impl_path = self._load_impl(current)
                if not impl_path:
                    FlowRepository.store_task_run(run_id, current, TaskOutcome.FAILURE.value, None, "impl not found")
                    break

                try:
                    task_instance = self._instantiate_task(impl_path)
                    FlowRepository.store_task_run(run_id, current, "running")
                    success, output = await task_instance.run({"previous_output": prev_output})
                except Exception as ex:
                    FlowRepository.store_task_run(run_id, current, TaskOutcome.FAILURE.value, None, f"exception: {ex}")
                    current = self._evaluate(conditions, current, succeeded=False)
                    continue

                FlowRepository.store_task_run(run_id, current, TaskOutcome.SUCCESS.value if success else TaskOutcome.FAILURE.value, output, None if success else "task returned failure")

                if not success:
                    current = self._evaluate(conditions, current, succeeded=False)
                    prev_output = output
                    if current == TaskOutcome.END.value:
                        break
                    continue

                # success
                prev_output = output
                current = self._evaluate(conditions, current, succeeded=True)
                if current == TaskOutcome.END.value:
                    break

            # finalize run status
            # If any task run had failure -> failed else success
            failures = 0
            with db_session() as db:
                failures = db.query(TaskRun).filter_by(run_id=run_id, status=TaskOutcome.FAILURE.value).count()
            FlowRepository.update_run_status(run_id, FlowRunStatus.FAILED if failures else FlowRunStatus.SUCCESS)
        except asyncio.CancelledError:
            FlowRepository.update_run_status(run_id, FlowRunStatus.CANCELLED)
        except Exception:
            FlowRepository.update_run_status(run_id, FlowRunStatus.FAILED)
        finally:
            # Your IDE might warn that "Coroutine 'pop' is not awaited" it can be ignored as pop is synchronous
            self.running_tasks.pop(run_id, None)
            self.cancellation_events.pop(run_id, None)

    @staticmethod
    def _evaluate(conditions: list[dict[str, Any]], source: str, succeeded: bool) -> str:
        matched = [c for c in conditions if c.get('source_task') == source]
        if not matched:
            return TaskOutcome.END.value
        cond = matched[0]
        if succeeded and cond.get('outcome') == TaskOutcome.SUCCESS.value:
            return cond.get('target_task_success', TaskOutcome.END.value)
        return cond.get('target_task_failure', TaskOutcome.END.value)

FLOW_MANAGER = FlowManager()
