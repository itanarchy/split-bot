from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.const import SITE_URL
from app.enums import PaginationMenuType

from .callback_data.gift_codes import CDCreateGiftCode
from .callback_data.menu import (
    CDLanguage,
    CDMenu,
    CDPagination,
    CDReferralProgram,
    CDTelegramPremium,
    CDTelegramStars,
)
from .callback_data.ton_connect import CDUnlinkWallet


def to_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.menu(), callback_data=CDMenu())
    return builder.as_markup()


def cancel_keyboard(i18n: I18nContext, data: CallbackData) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.cancel(), callback_data=data)
    return builder.as_markup()


def back_keyboard(i18n: I18nContext, data: CallbackData) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.back(), callback_data=data)
    return builder.as_markup()


def menu_keyboard(i18n: I18nContext, wallet_connected: bool) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.app(), web_app=WebAppInfo(url=SITE_URL))
    if wallet_connected:
        builder.button(text=i18n.buttons.premium(), callback_data=CDTelegramPremium())
        builder.button(text=i18n.buttons.stars(), callback_data=CDTelegramStars())
        builder.button(text=i18n.buttons.create_gift_code(), callback_data=CDCreateGiftCode())
        builder.button(text=i18n.buttons.referral_program(), callback_data=CDReferralProgram())
        builder.button(text=i18n.buttons.language(), callback_data=CDLanguage())
        builder.button(text=i18n.buttons.disconnect(), callback_data=CDUnlinkWallet())
        builder.adjust(1, 2, 1, 2, 1)
    else:
        builder.button(
            text=i18n.buttons.connect(),
            callback_data=CDPagination(type=PaginationMenuType.TON_WALLET),
        )
        builder.button(text=i18n.buttons.language(), callback_data=CDLanguage())
        builder.adjust(2, 1)
    return builder.as_markup()
