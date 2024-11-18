from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from app.enums import PaginationMenuType
from app.telegram.keyboards.callback_data.menu import CDPagination

if TYPE_CHECKING:
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper
    from app.telegram.helpers.paginator import Paginator

router: Final[Router] = Router(name=__name__)


# noinspection PyTypeChecker
@router.callback_query(CDPagination.filter(F.type == PaginationMenuType.TON_WALLET))
async def select_ton_wallet(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    ton_connect: TcAdapter,
    paginator: Paginator,
) -> Any:
    return await helper.answer(
        text=i18n.messages.choose_wallet(),
        reply_markup=paginator.choose_wallet_keyboard(
            i18n=i18n,
            wallets=await ton_connect.get_wallets(),
        ),
    )
