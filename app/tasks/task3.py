from typing import Any

from app.tasks import BaseTask
import asyncio

class Store(BaseTask):
    async def run(self, payload: dict[str, Any]) -> tuple[bool, Any]:
        await asyncio.sleep(0.1)
        return True, {"stored": True}
