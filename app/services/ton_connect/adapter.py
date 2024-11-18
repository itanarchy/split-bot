from __future__ import annotations

from contextlib import suppress
from typing import Any, Optional, cast

from pytonconnect import TonConnect
from pytonconnect.exceptions import WalletNotConnectedError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.dto.ton import TonWallet

from ..backend.types import Transaction
from ..database import RedisRepository
from .storage import TcStorage


class TcAdapter:
    manifest_url: str
    storage: TcStorage
    connector: TonConnect

    def __init__(
        self,
        manifest_url: str,
        telegram_id: int,
        session_pool: async_sessionmaker[AsyncSession],
        redis: RedisRepository,
        cache_time: int,
    ) -> None:
        self.manifest_url = manifest_url
        self.storage = TcStorage(
            telegram_id=telegram_id,
            session_pool=session_pool,
            redis=redis,
            cache_time=cache_time,
        )
        self.connector = TonConnect(manifest_url=manifest_url, storage=self.storage)

    def copy(self, telegram_id: int) -> TcAdapter:
        return TcAdapter(
            manifest_url=self.manifest_url,
            telegram_id=telegram_id,
            session_pool=self.storage.session_pool,
            redis=self.storage.redis,
            cache_time=self.storage.cache_time,
        )

    async def is_connected(self) -> bool:
        return cast(bool, await self.connector.restore_connection())

    async def get_address(self) -> Optional[str]:
        if await self.is_connected():
            return self.connector.account.address  # type: ignore
        return None

    async def get_wallets(self) -> list[TonWallet]:
        return [TonWallet.model_validate(wallet) for wallet in self.connector.get_wallets()]

    async def get_wallet(self, app_name: str) -> Optional[TonWallet]:
        wallets: list[TonWallet] = await self.get_wallets()
        for wallet in wallets:
            if wallet.app_name == app_name:
                return wallet
        return None

    async def generate_connection_url(self, wallet: TonWallet, ton_proof: str) -> str:
        return cast(
            str,
            await self.connector.connect(
                wallet=wallet.model_dump(),
                request={"ton_proof": ton_proof},
            ),
        )

    async def send_transaction(self, transaction: Transaction) -> dict[str, Any]:
        data: dict[str, Any] = transaction.model_dump(exclude_defaults=False)
        return cast(
            dict[str, Any],
            await self.connector.send_transaction(transaction=data),
        )

    async def disconnect(self) -> None:
        with suppress(WalletNotConnectedError):
            await self.connector.disconnect()
