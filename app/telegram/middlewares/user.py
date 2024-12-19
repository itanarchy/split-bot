from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import Bot, F
from aiogram.filters import CommandObject, CommandStart
from aiogram.filters.command import CommandException
from aiogram.types import Message, TelegramObject, Update
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware
from pytoniq_core import Address

from app.services.user import UserService
from app.telegram.middlewares.event_typed import EventTypedMiddleware
from app.utils.logging import database as logger

if TYPE_CHECKING:
    from app.models.dto import UserDto


class UserMiddleware(EventTypedMiddleware):
    def __init__(self) -> None:
        self.filter = CommandStart(magic=F.args.cast(Address).to_str(is_bounceable=True))

    async def resolve_inviter(self, event: TelegramObject, bot: Bot) -> Optional[str]:
        if isinstance(event, Update):
            event = event.event

        if not isinstance(event, Message) or event.text is None:
            return None

        try:
            command: CommandObject = await self.filter.parse_command(event.text, bot)
            return command.magic_result
        except CommandException:
            return None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[AiogramUser] = data.get("event_from_user")
        if aiogram_user is None or aiogram_user.is_bot:
            # Prevents the bot itself from being added to the database
            # when accepting chat_join_request and receiving chat_member updates.
            return await handler(event, data)

        user_service = data["user_service"] = UserService(
            session_pool=data["session_pool"],
            redis=data["redis"],
            config=data["config"],
        )

        user: Optional[UserDto] = await user_service.by_tg_id(telegram_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            user = await user_service.create(
                aiogram_user=aiogram_user,
                i18n_core=i18n.core,
                inviter=await self.resolve_inviter(event=event, bot=data["bot"]),
            )
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user
        return await handler(event, data)
