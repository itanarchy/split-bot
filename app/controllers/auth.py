from typing import Optional

from app.models.dto import TonConnectResult, UserDto
from app.services.backend import Backend
from app.services.backend.errors import SplitConflictError
from app.services.backend.types import User as SplitUser
from app.services.ton_connect import TcAdapter
from app.services.user import UserService


async def authorize_user(
    user: UserDto,
    result: TonConnectResult,
    backend: Backend,
    user_service: UserService,
    ton_connect: TcAdapter,
) -> None:
    by_address: Optional[UserDto] = await user_service.by_address(result.address)
    if by_address is not None:
        await logout_user(
            user=by_address,
            user_service=user_service,
            ton_connect=ton_connect.copy(telegram_id=by_address.telegram_id),
        )
    backend.access_token = result.access_token
    user.wallet_address = result.address
    old_token: Optional[str] = user.backend_access_token
    if old_token != result.access_token:
        user.backend_access_token = result.access_token
        try:
            split_user: SplitUser = await backend.create_user(inviter=user.inviter)
        except SplitConflictError:
            split_user = await backend.get_me()
        user.backend_user_id = split_user.id
        user.inviter = split_user.inviter
    await user_service.update(user=user)


async def logout_user(user: UserDto, user_service: UserService, ton_connect: TcAdapter) -> None:
    await user_service.update(
        user=user,
        wallet_address=None,
        backend_user_id=None,
        backend_access_token=None,
    )
    await ton_connect.disconnect()
