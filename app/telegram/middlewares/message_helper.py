from __future__ import annotations

from typing import Any, Awaitable, Callable, cast

from aiogram.types import CallbackQuery, ErrorEvent, Message, TelegramObject, Update

from app.enums import MiddlewareEventType
from app.telegram.helpers.messages import MessageHelper
from app.telegram.middlewares.event_typed import EventTypedMiddleware


class MessageHelperMiddleware(EventTypedMiddleware):
    __event_types__ = [
        MiddlewareEventType.MESSAGE,
        MiddlewareEventType.CALLBACK_QUERY,
        MiddlewareEventType.ERROR,
    ]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        update = event
        if isinstance(update, ErrorEvent):
            update = update.update
        if isinstance(update, Update):
            update = update.event
        data["helper"] = MessageHelper(
            update=cast(Message | CallbackQuery, update),
            bot=data["bot"],
            fsm=data["state"],
            i18n=data["i18n"],
        )
        return await handler(event, data)
