from typing import Any

from app.tasks import BaseTask
import asyncio

class Fetch(BaseTask):
    async def run(self, payload: dict[str, Any]) -> tuple[bool, Any]:
        await asyncio.sleep(0.2)
        return True, {"items":[1,2,3]}
