from typing import Any

class BaseTask:
    async def run(self, payload: dict[str, Any]) -> tuple[bool, Any]:
        raise NotImplementedError
