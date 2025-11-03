import json
from datetime import datetime

from app.db.flow import Flow, FlowRun
from app.db.run import TaskRun, TaskRegistry
from app.db import db_session
from typing import Any
from app.models.flow import Flow as FlowModel
from app.utils.enums import FlowRunStatus


class FlowRepository:
    @staticmethod
    def create_flow(flow: FlowModel):
        flow_id = flow.id
        with db_session() as db:
            existing = db.get(Flow, flow_id)
            if existing:
                raise ValueError("flow already exists")
            f = Flow(id=flow_id, name=flow.name, payload=flow.model_dump_json())
            db.add(f)
            db.flush()
            return flow_id

    @staticmethod
    def list_flows():
        with db_session() as db:
            flows: list[Flow] = db.query(Flow).all()
            return [{
                'id': flow.id,
                'name': flow.name,
                'payload': flow.payload,
                'created_at': flow.created_at,
            } for flow in flows]

    @staticmethod
    def get_flow(flow_id: str) -> dict[str, Any] | None:
        with db_session() as db:
            f = db.get(Flow, flow_id)
            return json.loads(f.payload) if f else None

    @staticmethod
    def create_run(run_id: str, flow_id: str, status: str):
        with db_session() as db:
            r = FlowRun(id=run_id, flow_id=flow_id, status=status)
            db.add(r)

    @staticmethod
    def update_run_status(run_id: str, status: FlowRunStatus):
        with db_session() as db:
            r = db.get(FlowRun, run_id)
            if r:
                if status in (FlowRunStatus.SUCCESS, FlowRunStatus.FAILED, FlowRunStatus.CANCELLED):
                    r.finished_at = datetime.now()
                r.status = status.value
                db.commit()

    @staticmethod
    def store_task_run(run_id: str, task_name: str, status: str, output: Any = None, error: str | None = None):
        with db_session() as db:
            tr = db.query(TaskRun).filter_by(run_id=run_id, task_name=task_name).first()
            if tr:
                tr.status = status
                tr.output = json.dumps(output, default=str) if output is not None else None
                tr.error = error
                tr.finished_at = datetime.now()
            else:
                tr = TaskRun(
                    run_id=run_id,
                    task_name=task_name,
                    status=status,
                    output=json.dumps(output, default=str) if output is not None else None,
                    error=error
                )
                db.add(tr)
            db.commit()

    @staticmethod
    def list_runs(flow_id: str):
        with db_session() as db:
            runs = db.query(FlowRun).filter_by(flow_id=flow_id).order_by(FlowRun.started_at.desc()).all()
            return [{"run_id": r.id, "status": r.status, "started_at": r.started_at, "finished_at": r.finished_at} for r
                    in runs]

    @staticmethod
    def get_run(run_id: str):
        with db_session() as db:
            r = db.get(FlowRun, run_id)
            if not r:
                return None
            tasks = db.query(TaskRun).filter_by(run_id=run_id).order_by(TaskRun.id).all()
            tasks = [{
                "task_name": t.task_name,
                "status": t.status,
                "output": json.loads(t.output) if t.output else None,
                "error": t.error,
                "started_at": t.started_at,
                "finished_at": t.finished_at,
            } for t in tasks]
            flow = {"run_id": r.id, "flow_id": r.flow_id, "status": r.status}
            return flow, tasks


class TaskRegistryRepo:
    @staticmethod
    def get_all_tasks() -> list[dict[str, str]]:
        with db_session() as db:
            rows = db.query(TaskRegistry).all()
            return [{"task_name": row.task_name, "impl_path": row.impl_path} for row in rows]

    @staticmethod
    def get_impl_for(task_name: str) -> str | None:
        with db_session() as db:
            row = db.query(TaskRegistry).filter_by(task_name=task_name).first()
            return row.impl_path if row else None

    @staticmethod
    def register_task(task_name: str, impl_path: str):
        with db_session() as db:
            existing = db.query(TaskRegistry).filter_by(task_name=task_name).first()
            if existing:
                existing.impl_path = impl_path
            else:
                db.add(TaskRegistry(task_name=task_name, impl_path=impl_path))
