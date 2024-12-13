from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.utils.localization.patches import FluentBool

from .callback_data.menu import CDMenu, CDSetLanguage


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
