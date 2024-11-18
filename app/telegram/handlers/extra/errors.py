from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from aiogram_i18n import I18nContext

from app.controllers.auth import logout_user
from app.exceptions.base import BotError
from app.models.dto import UserDto
from app.services.backend.errors import SplitUnauthorizedError
from app.services.user import UserService
from app.telegram.keyboards.ton_connect import connect_wallet_keyboard

if TYPE_CHECKING:
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.error(ExceptionTypeFilter(BotError), F.update.message)
async def handle_some_error(error: ErrorEvent, i18n: I18nContext) -> Any:
    await error.update.message.answer(text=i18n.messages.something_went_wrong())


@router.error(ExceptionTypeFilter(SplitUnauthorizedError))
async def expire_session(
    _: ErrorEvent,
    helper: MessageHelper,
    i18n: I18nContext,
    user: UserDto,
    user_service: UserService,
    ton_connect: TcAdapter,
) -> Any:
    await logout_user(user=user, user_service=user_service, ton_connect=ton_connect)
    return await helper.edit_current_message(
        text=i18n.messages.wallet_not_connected(),
        reply_markup=connect_wallet_keyboard(i18n=i18n),
    )
