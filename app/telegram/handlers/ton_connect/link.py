from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import WalletAlreadyConnectedError

from app.controllers.auth import authorize_user
from app.controllers.ton.connect import generate_ton_connection
from app.controllers.ton.waiter import wait_until_connected
from app.exceptions.ton_connect import InvalidTonProofError
from app.models.dto import UserDto
from app.services.backend import Backend
from app.telegram.handlers.menu.main import show_main_menu
from app.telegram.helpers.exceptions import silent_bot_request
from app.telegram.keyboards.callback_data.ton_connect import CDCancelConnection, CDChooseWallet
from app.telegram.keyboards.menu import to_menu_keyboard
from app.telegram.keyboards.ton_connect import ton_connect_keyboard
from app.utils.qr import create_qr_code
from app.utils.ton import short_address

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.models.dto.ton import TonConnection, TonConnectResult
    from app.services.task_manager import TaskManager
    from app.services.ton_connect import TcAdapter
    from app.services.user import UserService
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


async def _handle_ton_connection(
    message: Message,
    i18n: I18nContext,
    user: UserDto,
    user_service: UserService,
    ton_connect: TcAdapter,
    backend: Backend,
    assets: Assets,
) -> Any:
    try:
        result: TonConnectResult = await wait_until_connected(
            ton_connect=ton_connect,
            backend=backend,
            timeout=assets.ton_connect.timeout,
        )
    except (TimeoutError, InvalidTonProofError):
        with silent_bot_request():
            await message.delete()
        return await message.answer(
            text=i18n.messages.connection_timeout(),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )

    await authorize_user(
        user=user,
        result=result,
        ton_connect=ton_connect,
        user_service=user_service,
        backend=backend,
    )

    with silent_bot_request():
        await message.delete()
    await message.answer(
        text=i18n.messages.wallet_connected(
            address=html.link(
                value=short_address(address=result.address),
                link=f"https://tonviewer.com/{result.address}",
            ),
        ),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )


@router.callback_query(CDChooseWallet.filter())
async def choose_wallet(
    query: CallbackQuery,
    helper: MessageHelper,
    callback_data: CDChooseWallet,
    i18n: I18nContext,
    state: FSMContext,
    user: UserDto,
    user_service: UserService,
    ton_connect: TcAdapter,
    backend: Backend,
    assets: Assets,
    task_manager: TaskManager,
) -> Any:
    try:
        connection: TonConnection = await generate_ton_connection(
            wallet_name=callback_data.wallet_name,
            backend=backend,
            tc_adapter=ton_connect,
        )
    except WalletAlreadyConnectedError:
        return await show_main_menu(_=query, helper=helper, i18n=i18n, state=state, user=user)
    with silent_bot_request():
        await query.message.delete()
    message: Message = await query.message.answer_photo(
        photo=BufferedInputFile(
            file=await create_qr_code(url=connection.url),
            filename=f"{connection.id}.png",
        ),
        caption=i18n.messages.ton_connect(),
        reply_markup=ton_connect_keyboard(i18n=i18n, connection=connection),
    )
    task_manager.run_task(
        task_name=connection.id,
        coro=_handle_ton_connection(
            message=message,
            i18n=i18n,
            user=user,
            user_service=user_service,
            ton_connect=ton_connect,
            backend=backend,
            assets=assets,
        ),
    )


@router.callback_query(CDCancelConnection.filter())
async def cancel_connection(
    query: CallbackQuery,
    callback_data: CDCancelConnection,
    i18n: I18nContext,
    task_manager: TaskManager,
) -> Any:
    await task_manager.cancel_task(task_name=callback_data.task_id)
    with silent_bot_request():
        await query.message.delete()
    return await query.message.answer(
        text=i18n.messages.connection_cancelled(),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )
