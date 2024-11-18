from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from app.models.sql import TcRecord

from .base import BaseRepository


# noinspection PyTypeChecker
class TonConnectRepository(BaseRepository):
    async def remove_record(self, telegram_id: int, key: str) -> bool:
        return await self._delete(
            TcRecord,
            TcRecord.telegram_id == telegram_id,
            TcRecord.key == key,
        )

    async def get_record_value(self, telegram_id: int, key: str) -> Optional[str]:
        return await self._get(
            TcRecord.value,
            TcRecord.telegram_id == telegram_id,
            TcRecord.key == key,
        )

    async def set_record(self, telegram_id: int, key: str, value: str) -> None:
        query = (
            insert(TcRecord)
            .values(telegram_id=telegram_id, key=key, value=value)
            .on_conflict_do_update(
                index_elements=["telegram_id", "key"],
                set_={"value": value},
            )
        )
        await self.session.execute(query)
        await self.session.commit()
