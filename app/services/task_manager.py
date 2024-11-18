from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Any, Coroutine, Optional


class TaskManager:
    tasks: dict[str, asyncio.Task[Any]]

    def __init__(self) -> None:
        self.tasks = {}

    def run_task(self, task_name: str, coro: Coroutine[Any, Any, Any]) -> None:
        if task_name in self.tasks:
            raise ValueError(f"Task {task_name} is already running")
        task = self.tasks[task_name] = asyncio.create_task(coro=coro)
        task.add_done_callback(lambda _: self.tasks.pop(task_name, None))

    async def cancel_task(self, task_name: str) -> None:
        task: Optional[asyncio.Task[Any]] = self.tasks.pop(task_name, None)
        if task is None:
            return
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
