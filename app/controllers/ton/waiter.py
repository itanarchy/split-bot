import asyncio

from pytonconnect import TonConnect

from app.controllers.ton.proof import verify_ton_proof
from app.models.dto import TonConnectResult
from app.services.backend import Backend
from app.services.ton_connect import TcAdapter
from app.utils.ton import convert_address


# noinspection PyProtectedMember
async def wait_until_connected(
    ton_connect: TcAdapter,
    timeout: int,
    backend: Backend,
) -> TonConnectResult:
    connector: TonConnect = ton_connect.connector
    for _ in range(timeout):
        await asyncio.sleep(1)
        if not connector.connected or not connector.account or not connector.account.address:
            continue
        return TonConnectResult(
            address=convert_address(connector.account),
            access_token=await verify_ton_proof(connector=connector, backend=backend),
        )
    raise TimeoutError("Connection timeout")
