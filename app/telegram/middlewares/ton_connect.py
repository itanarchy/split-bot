from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional

from aiogram.types import TelegramObject

from app.controllers.auth import logout_user
from app.services.ton_connect import TcAdapter
from app.telegram.middlewares.event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from app.models.config import AppConfig, Assets
    from app.models.dto import UserDto


class TonConnectMiddleware(EventTypedMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: Optional[UserDto] = data.get("user")
        if user is None:
            return await handler(event, data)
        assets: Assets = data["assets"]
        config: AppConfig = data["config"]
        data["ton_connect"] = adapter = TcAdapter(
            manifest_url=assets.ton_connect.manifest_url,
            telegram_id=user.telegram_id,
            session_pool=data["session_pool"],
            redis=data["redis"],
            cache_time=config.common.ton_connect_cache_time,
        )
        if user.wallet_connected and not await adapter.is_connected():
            await logout_user(user=user, user_service=data["user_service"], ton_connect=adapter)
        return await handler(event, data)
