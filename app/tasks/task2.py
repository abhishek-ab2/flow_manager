from typing import Any

from app.tasks import BaseTask
import asyncio

class Process(BaseTask):
    async def run(self, payload: dict[str, Any]) -> tuple[bool, Any]:
        await asyncio.sleep(0.2)
        prev = payload.get("previous_output")
        if not prev:
            return False, None
        s = sum(prev.get("items", []))
        return True, {"sum": s}
