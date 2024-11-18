from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.controllers.auth import logout_user
from app.models.dto import UserDto
from app.services.user import UserService
from app.telegram.keyboards.callback_data.ton_connect import CDUnlinkWallet

from ..menu.main import show_main_menu

if TYPE_CHECKING:
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.callback_query(CDUnlinkWallet.filter())
async def unlink_wallet(
    _: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    user: UserDto,
    user_service: UserService,
    ton_connect: TcAdapter,
) -> Any:
    await logout_user(user=user, user_service=user_service, ton_connect=ton_connect)
    await show_main_menu(_=_, helper=helper, i18n=i18n, state=state, user=user)
