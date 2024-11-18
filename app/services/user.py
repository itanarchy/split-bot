from typing import Any, Awaitable, Callable, Optional, cast

from aiogram.types import User as AiogramUser
from aiogram_i18n.cores import BaseCore

from app.models.config import AppConfig
from app.models.dto import UserDto
from app.models.sql import User
from app.services.database import RedisRepository
from app.services.database.postgres import UsersRepository


class UserService:
    def __init__(
        self,
        repository: UsersRepository,
        redis: RedisRepository,
        config: AppConfig,
    ) -> None:
        self.repository = repository
        self.redis = redis
        self.config = config

    async def create(
        self,
        aiogram_user: AiogramUser,
        i18n_core: BaseCore[Any],
        inviter: Optional[str] = None,
    ) -> UserDto:
        user: User = User(
            telegram_id=aiogram_user.id,
            name=aiogram_user.full_name,
            locale=(
                aiogram_user.language_code
                if aiogram_user.language_code in i18n_core.locales
                else cast(str, i18n_core.default_locale)
            ),
            inviter=inviter,
        )
        await self.repository.uow.commit(user)
        return user.dto()

    async def _get(
        self,
        getter: Callable[[Any], Awaitable[Optional[User]]],
        key: Any,
    ) -> Optional[UserDto]:
        user_dto: Optional[UserDto] = await self.redis.get_user(key=key)
        if user_dto is not None:
            return user_dto
        user: Optional[User] = await getter(key)
        if user is None:
            return None
        await self.redis.save_user(
            key=user.telegram_id,
            value=(user_dto := user.dto()),
            cache_time=self.config.common.users_cache_time,
        )
        return user_dto

    async def get(self, user_id: int) -> Optional[UserDto]:
        return await self._get(self.repository.get, user_id)

    async def by_tg_id(self, telegram_id: int) -> Optional[UserDto]:
        return await self._get(self.repository.by_tg_id, telegram_id)

    async def by_address(self, wallet_address: str) -> Optional[UserDto]:
        return await self._get(self.repository.by_address, wallet_address)

    async def update(self, user: UserDto, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.repository.update(user_id=user.id, **user.model_state)
        await self.redis.save_user(
            key=user.telegram_id,
            value=user,
            cache_time=self.config.common.users_cache_time,
        )
