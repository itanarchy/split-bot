from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from .ton_connect import TonConnectRepository
from .users import UsersRepository


class Repository(BaseRepository):
    users: UsersRepository
    ton_connect: TonConnectRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.ton_connect = TonConnectRepository(session=session)
        self.users = UsersRepository(session=session)
