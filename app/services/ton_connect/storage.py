import logging
from typing import Final, Optional

from pytonconnect.storage import IStorage
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.services.database import RedisRepository, Repository

logger: Final[logging.Logger] = logging.getLogger(name=__name__)


class TcStorage(IStorage):  # type: ignore
    def __init__(
        self,
        telegram_id: int,
        session_pool: async_sessionmaker[AsyncSession],
        redis: RedisRepository,
        cache_time: int,
    ) -> None:
        self.telegram_id = telegram_id
        self.session_pool = session_pool
        self.redis = redis
        self.cache_time = cache_time

    async def set_item(self, key: str, value: str) -> None:
        async with self.session_pool() as session:
            repository: Repository = Repository(session=session)
            try:
                await repository.ton_connect.set_record(
                    telegram_id=self.telegram_id,
                    key=key,
                    value=value,
                )
                await self.redis.set_tc_record(
                    telegram_id=self.telegram_id,
                    key=key,
                    value=value,
                    cache_time=self.cache_time,
                )
            except IntegrityError:
                logger.error("Failed to set record %s for user %d", key, self.telegram_id)

    async def _get_from_db(self, key: str) -> Optional[str]:
        async with self.session_pool() as session:
            repository: Repository = Repository(session=session)
            value: Optional[str] = await repository.ton_connect.get_record_value(
                telegram_id=self.telegram_id,
                key=key,
            )

        if value is not None:
            await self.redis.set_tc_record(
                telegram_id=self.telegram_id,
                key=key,
                value=value,
                cache_time=self.cache_time,
            )

        return value

    async def get_item(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        tc_record_value: Optional[str] = await self.redis.get_tc_record(
            telegram_id=self.telegram_id,
            key=key,
        )
        if tc_record_value is None:
            tc_record_value = await self._get_from_db(key=key)
        return tc_record_value or default_value

    async def remove_item(self, key: str) -> None:
        async with self.session_pool() as session:
            repository: Repository = Repository(session=session)
            await repository.ton_connect.remove_record(telegram_id=self.telegram_id, key=key)
            await self.redis.delete_tc_record(telegram_id=self.telegram_id, key=key)
