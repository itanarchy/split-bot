from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.managers import BaseManager

from app.services.user import UserService

if TYPE_CHECKING:
    from app.models.dto import UserDto


class UserManager(BaseManager):
    async def get_locale(
        self,
        event_from_user: Optional[AiogramUser] = None,
        user: Optional[UserDto] = None,
    ) -> str:
        if user is not None:
            return user.locale
        if event_from_user and event_from_user.language_code is not None:
            return event_from_user.language_code
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: UserDto, user_service: UserService) -> None:
        await user_service.update(user=user, locale=locale)
