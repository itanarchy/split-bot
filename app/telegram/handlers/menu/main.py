from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from aiogram.utils.deep_linking import create_start_link
from aiogram_i18n import I18nContext

from app.telegram.keyboards.callback_data.menu import CDMenu, CDReferralProgram
from app.telegram.keyboards.menu import menu_keyboard, referral_program_keyboard

if TYPE_CHECKING:
    from app.models.dto import UserDto
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(CDMenu.filter())
async def show_main_menu(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    user: UserDto,
) -> Any:
    await state.clear()
    return await helper.answer(
        text=i18n.messages.hello(name=user.mention),
        reply_markup=menu_keyboard(i18n=i18n, wallet_connected=user.wallet_connected),
    )


@router.callback_query(CDReferralProgram.filter())
async def show_referral_link(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    bot: Bot,
    user: UserDto,
) -> Any:
    if user.wallet_address is None:
        return await helper.answer(
            text=i18n.messages.wallet_not_connected(),
            reply_markup=menu_keyboard(i18n=i18n, wallet_connected=user.wallet_connected),
        )

    url: str = await create_start_link(bot=bot, payload=user.wallet_address)
    return await helper.answer(
        text=i18n.messages.referral.info(link=url),
        reply_markup=referral_program_keyboard(i18n=i18n, link=url),
    )
