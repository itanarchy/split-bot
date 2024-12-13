from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.const import SITE_URL
from app.enums import PaginationMenuType
from app.utils.localization.patches import FluentBool

from .callback_data.menu import (
    CDLanguage,
    CDMenu,
    CDPagination,
    CDReferralProgram,
    CDSetLanguage,
    CDTelegramPremium,
    CDTelegramStars,
)
from .callback_data.ton_connect import CDUnlinkWallet


def to_menu_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.menu(), callback_data=CDMenu())
    return builder.as_markup()


def menu_keyboard(i18n: I18nContext, wallet_connected: bool) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.app(), web_app=WebAppInfo(url=SITE_URL))
    if wallet_connected:
        builder.button(text=i18n.buttons.premium(), callback_data=CDTelegramPremium())
        builder.button(text=i18n.buttons.stars(), callback_data=CDTelegramStars())
        builder.button(text=i18n.buttons.referral_program(), callback_data=CDReferralProgram())
        builder.button(text=i18n.buttons.language(), callback_data=CDLanguage())
        builder.button(text=i18n.buttons.disconnect(), callback_data=CDUnlinkWallet())
        builder.adjust(1, 2, 2, 1)
    else:
        builder.button(
            text=i18n.buttons.connect(),
            callback_data=CDPagination(type=PaginationMenuType.TON_WALLET),
        )
        builder.button(text=i18n.buttons.language(), callback_data=CDLanguage())
        builder.adjust(2, 1)
    return builder.as_markup()


def referral_program_keyboard(i18n: I18nContext, link: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.buttons.copy_link(),
        copy_text=CopyTextButton(text=i18n.messages.referral.invite(link=link)),
    )
    builder.button(text=i18n.buttons.back(), callback_data=CDMenu())
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def language_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for locale in i18n.core.available_locales:
        builder.button(
            text=i18n.extra.selectable(
                value=i18n.get("extra-language", locale),
                selected=FluentBool(locale == i18n.locale),
            ),
            callback_data=CDSetLanguage(locale=locale),
        )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text=i18n.buttons.back(), callback_data=CDMenu().pack()))
    return builder.as_markup()
