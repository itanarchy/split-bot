from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.enums import GiftCodeCreationStatus

from .callback_data.gift_codes import (
    CDConfirmGiftCode,
    CDSetGiftCodeActivations,
    CDSetGiftCodeAmount,
)
from .callback_data.menu import CDMenu


def gift_code_creation_keyboard(
    i18n: I18nContext, status: GiftCodeCreationStatus
) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    sizes: list[int] = [2, 1]
    if status == GiftCodeCreationStatus.READY:
        sizes.insert(0, 1)
        builder.button(text=i18n.buttons.create(), callback_data=CDConfirmGiftCode())
    builder.button(
        text=i18n.buttons.set_gift_code_activations(),
        callback_data=CDSetGiftCodeActivations(),
    )
    builder.button(
        text=i18n.buttons.set_gift_code_amount(),
        callback_data=CDSetGiftCodeAmount(),
    )
    builder.button(text=i18n.buttons.back(), callback_data=CDMenu())
    builder.adjust(*sizes)
    return builder.as_markup()
