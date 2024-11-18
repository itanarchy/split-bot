from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.models.dto.ton import TonConnection, TonWallet

from ...enums import PaginationMenuType
from .callback_data.menu import CDMenu, CDPagination
from .callback_data.ton_connect import CDCancelConnection, CDChooseWallet


def connect_wallet_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.buttons.connect(),
        callback_data=CDPagination(type=PaginationMenuType.TON_WALLET),
    )
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def choose_wallet_keyboard(i18n: I18nContext, wallets: list[TonWallet]) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for wallet in wallets:
        builder.button(
            text=wallet.name,
            callback_data=CDChooseWallet(wallet_name=wallet.app_name),
        )
    builder.button(text=i18n.buttons.back(), callback_data=CDMenu())
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def ton_connect_keyboard(i18n: I18nContext, connection: TonConnection) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.button(text=i18n.buttons.ton_connect_url(), url=connection.url)
    builder.button(
        text=i18n.buttons.cancel(),
        callback_data=CDCancelConnection(task_id=connection.id),
    )
    builder.adjust(1, repeat=True)
    return builder.as_markup()
