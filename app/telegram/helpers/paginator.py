from aiogram.contrib.paginator import Paginator as _Paginator
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InlineKeyboardButton

from app.enums import PaginationMenuType
from app.models.dto import TonWallet

from ..keyboards.callback_data.menu import CDMenu
from ..keyboards.callback_data.ton_connect import CDChooseWallet


def get_wallet_button(wallet: TonWallet) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=wallet.name,
        callback_data=CDChooseWallet(wallet_name=wallet.app_name).pack(),
    )


class Paginator(_Paginator):
    def choose_wallet_keyboard(
        self,
        i18n: I18nContext,
        wallets: list[TonWallet],
    ) -> InlineKeyboardMarkup:
        self.recalculate_offset(total_count=len(wallets))
        builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        builder.button(text=i18n.buttons.back(), callback_data=CDMenu())
        return self.get_keyboard(
            objects=wallets[self.offset : self.offset + self.rows_per_page],
            button_getter=get_wallet_button,
            menu_type=PaginationMenuType.TON_WALLET,
            attach=builder,
        )
