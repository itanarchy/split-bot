from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.types import TelegramObject

from app.services.backend import Backend
from app.services.backend.session import BackendSession
from app.telegram.middlewares.event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from app.models.config import AppConfig
    from app.models.dto import UserDto


class BackendProviderMiddleware(EventTypedMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[UserDto] = data.get("user")
        if user is None:
            return await handler(event, data)
        config: AppConfig = data["config"]
        session: BackendSession = data["backend_session"]
        data["backend"] = Backend(
            base_url=config.common.backend_url,
            access_token=user.backend_access_token,
            session=session,
        )
        return await handler(event, data)
