from __future__ import annotations

from typing import Final

from aiogram import Bot, Router
from aiogram.types import BotCommand

from app.services.backend.session import BackendSession

router: Final[Router] = Router(name=__name__)


@router.startup()
async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(commands=[BotCommand(command="start", description="Main menu")])


@router.shutdown()
async def on_shutdown(bot: Bot, backend_session: BackendSession) -> None:
    await bot.session.close()
    await backend_session.close()
