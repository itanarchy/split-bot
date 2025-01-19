from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional
from uuid import UUID

from aiogram import Bot, F
from aiogram.filters import CommandObject, CommandStart
from aiogram.filters.command import CommandException
from aiogram.types import Message, TelegramObject, Update
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware
from pytoniq_core import Address

from app.services.deep_links import DeepLinksService
from app.services.user import UserService
from app.telegram.middlewares.event_typed import EventTypedMiddleware
from app.utils.logging import database as logger

if TYPE_CHECKING:
    from app.models.dto import DeepLinkDto, UserDto


class UserMiddleware(EventTypedMiddleware):
    def __init__(self) -> None:
        self.deep_links_filter = CommandStart(magic=F.args.cast(UUID))
        self.address_filter = CommandStart(magic=F.args.cast(Address).to_str(is_bounceable=True))

    async def resolve_inviter(
        self,
        event: TelegramObject,
        bot: Bot,
        user_service: UserService,
        deep_links: DeepLinksService,
    ) -> Optional[str]:
        if isinstance(event, Update):
            event = event.event

        if not isinstance(event, Message) or event.text is None:
            return None

        with suppress(CommandException):
            command: CommandObject = await self.address_filter.parse_command(event.text, bot)
            return command.magic_result

        with suppress(CommandException, ValueError):
            command = await self.deep_links_filter.parse_command(event.text, bot)
            if not isinstance(command.magic_result, UUID):
                raise ValueError()
            deep_link: Optional[DeepLinkDto] = await deep_links.get(link_id=command.magic_result)
            if deep_link is None:
                raise ValueError()
            owner: Optional[UserDto] = await user_service.get(user_id=deep_link.owner_id)
            if owner is None:
                raise ValueError()
            return owner.wallet_address

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

        user_service: UserService = data["user_service"]
        user: Optional[UserDto] = await user_service.by_tg_id(telegram_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            user = await user_service.create(
                aiogram_user=aiogram_user,
                i18n_core=i18n.core,
                inviter=await self.resolve_inviter(
                    event=event,
                    bot=data["bot"],
                    user_service=user_service,
                    deep_links=data["deep_links"],
                ),
            )
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user
        return await handler(event, data)
