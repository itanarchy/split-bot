from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from app.telegram.keyboards.callback_data.menu import CDLanguage, CDSetLanguage
from app.telegram.keyboards.language import language_keyboard

if TYPE_CHECKING:
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.callback_query(CDLanguage.filter())
async def show_language_menu(_: TelegramObject, helper: MessageHelper, i18n: I18nContext) -> Any:
    return await helper.answer(
        text=i18n.messages.language(),
        reply_markup=language_keyboard(i18n=i18n),
    )


@router.callback_query(CDSetLanguage.filter())
async def set_language(
    _: TelegramObject,
    callback_data: CDSetLanguage,
    helper: MessageHelper,
    i18n: I18nContext,
) -> Any:
    await i18n.set_locale(locale=callback_data.locale)
    return await show_language_menu(_, helper, i18n)
