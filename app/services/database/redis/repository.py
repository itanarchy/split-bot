from __future__ import annotations

from typing import Any, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.models.dto import DeepLinkDto, UserDto
from app.utils import mjson
from app.utils.key_builder import StorageKey

from .keys import DeepLinkKey, TcRecordKey, UserKey

T = TypeVar("T", bound=Any)


class RedisRepository:
    def __init__(self, client: Redis) -> None:
        self.client = client

    async def get(self, key: StorageKey, validator: type[T]) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return None
        value = mjson.decode(value)
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def delete(self, key: StorageKey) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    async def set_tc_record(
        self,
        telegram_id: int,
        key: str,
        value: str,
        cache_time: int,
    ) -> None:
        tc_record_key: TcRecordKey = TcRecordKey(telegram_id=telegram_id, key=key)
        await self.client.set(name=tc_record_key.pack(), value=value, ex=cache_time)

    async def get_tc_record(self, telegram_id: int, key: str) -> Optional[str]:
        tc_record_key: TcRecordKey = TcRecordKey(telegram_id=telegram_id, key=key)
        result: Optional[bytes] = await self.client.get(tc_record_key.pack())
        if result is not None:
            return result.decode()
        return None

    async def delete_tc_record(self, telegram_id: int, key: str) -> None:
        await self.delete(key=TcRecordKey(telegram_id=telegram_id, key=key))

    async def save_user(self, key: Any, value: UserDto, cache_time: int) -> None:
        await self.set(key=UserKey(key=str(key)), value=value, ex=cache_time)

    async def get_user(self, key: Any) -> Optional[UserDto]:
        return await self.get(key=UserKey(key=str(key)), validator=UserDto)

    async def delete_user(self, key: Any) -> None:
        await self.delete(key=UserKey(key=str(key)))

    async def save_deep_link(self, link: DeepLinkDto, cache_time: int) -> None:
        await self.set(key=DeepLinkKey(id=link.id), value=link, ex=cache_time)

    async def get_deep_link(self, link_id: UUID) -> Optional[DeepLinkDto]:
        return await self.get(key=DeepLinkKey(id=link_id), validator=DeepLinkDto)
