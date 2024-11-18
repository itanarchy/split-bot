from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram import Bot
from aiogram.types import Chat, TelegramObject
from aiogram_i18n import I18nContext

from app.telegram.keyboards.ton_connect import connect_wallet_keyboard

from .event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from app.models.sql import User


class TonConnectCheckerMiddleware(EventTypedMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: Optional[User] = data.get("user")
        if user is None:
            return await handler(event, data)
        if not user.wallet_address:
            chat: Chat = data["event_chat"]
            bot: Bot = data["bot"]
            i18n: I18nContext = data["i18n"]
            return await bot.send_message(
                chat_id=chat.id,
                text=i18n.messages.wallet_not_connected(),
                reply_markup=connect_wallet_keyboard(i18n=i18n),
            )
        return await handler(event, data)
