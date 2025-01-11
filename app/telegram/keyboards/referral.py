from aiogram.types import CopyTextButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from .callback_data.menu import CDMenu


def referral_program_keyboard(i18n: I18nContext, url: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.buttons.copy_link(),
        copy_text=CopyTextButton(text=i18n.messages.referral.invite(link=url)),
    )
    builder.button(text=i18n.buttons.share(), switch_inline_query="")
    builder.button(text=i18n.buttons.back(), callback_data=CDMenu())
    builder.adjust(2, 1, repeat=True)
    return builder.as_markup()


def join_bot_keyboard(i18n: I18nContext, url: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.join_bot(), url=url)
    return builder.as_markup()


def share_keyboard(i18n: I18nContext, deep_link_id: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.share(), switch_inline_query=deep_link_id)
    return builder.as_markup()
