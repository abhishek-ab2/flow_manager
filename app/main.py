
from fastapi import FastAPI
from .controllers import tasks, flows, runs

app = FastAPI(title="Flow Manager API")

app.include_router(tasks.router)
app.include_router(flows.router)
app.include_router(runs.router)
