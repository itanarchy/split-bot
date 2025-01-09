from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InlineKeyboardButton

from app.models.config import Assets
from app.telegram.keyboards.callback_data.menu import CDMenu
from app.telegram.keyboards.callback_data.purchase import (
    CDConfirmPurchase,
    CDSelectCurrency,
    CDSelectSubscriptionPeriod,
    CDSelectUsername,
)


def enter_username_keyboard(
    i18n: I18nContext,
    username: Optional[str] = None,
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if username is not None:
        builder.button(
            text=i18n.buttons.select_username(username=username),
            callback_data=CDSelectUsername(username=username),
        )
    builder.button(text=i18n.buttons.menu(), callback_data=CDMenu())
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def subscription_period_keyboard(i18n: I18nContext, assets: Assets) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for period in assets.shop.subscription_periods:
        builder.button(
            text=i18n.messages.purchase.subscription_period(period=period),
            callback_data=CDSelectSubscriptionPeriod(period=period),
        )
    builder.adjust(3, repeat=True)
    back: InlineKeyboardButton = InlineKeyboardButton(
        text=i18n.buttons.menu(),
        callback_data=CDMenu().pack(),
    )
    builder.row(back)
    return builder.as_markup()


def currency_keyboard(i18n: I18nContext, assets: Assets) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for currency in assets.shop.available_tickers:
        builder.button(text=currency, callback_data=CDSelectCurrency(currency=currency))
    builder.adjust(3, repeat=True)
    back: InlineKeyboardButton = InlineKeyboardButton(
        text=i18n.buttons.menu(),
        callback_data=CDMenu().pack(),
    )
    builder.row(back)
    return builder.as_markup()


def confirm_purchase_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.confirm(), callback_data=CDConfirmPurchase())
    builder.button(text=i18n.buttons.cancel(), callback_data=CDMenu())
    return builder.as_markup()
