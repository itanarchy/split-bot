from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from app.models.dto import TonConnection
from app.services.backend import Backend

if TYPE_CHECKING:
    from app.models.dto import TonWallet
    from app.services.ton_connect import TcAdapter


async def generate_ton_connection(
    wallet_name: str,
    tc_adapter: TcAdapter,
    backend: Backend,
) -> TonConnection:
    wallet: Optional[TonWallet] = await tc_adapter.get_wallet(app_name=wallet_name)
    if wallet is None:
        raise ValueError("Wallet not found")
    ton_proof: str = await backend.generate_ton_proof_payload()
    return TonConnection(
        url=await tc_adapter.generate_connection_url(wallet=wallet, ton_proof=ton_proof),
        ton_proof=ton_proof,
    )
