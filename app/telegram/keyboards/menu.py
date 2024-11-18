from aiogram.types import CopyTextButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.enums import PaginationMenuType

from .callback_data.menu import (
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


def menu_keyboard(i18n: I18nContext, wallet_connected: bool) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if wallet_connected:
        builder.button(text=i18n.buttons.premium(), callback_data=CDTelegramPremium())
        builder.button(text=i18n.buttons.stars(), callback_data=CDTelegramStars())
        builder.button(text=i18n.buttons.referral_program(), callback_data=CDReferralProgram())
        builder.button(text=i18n.buttons.disconnect(), callback_data=CDUnlinkWallet())
        builder.adjust(2, 1, 1)
    else:
        builder.button(
            text=i18n.buttons.connect(),
            callback_data=CDPagination(type=PaginationMenuType.TON_WALLET),
        )
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
