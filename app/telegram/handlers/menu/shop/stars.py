from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import UserRejectsError

from app.controllers.price import PriceDto, get_stars_price
from app.telegram.filters import MagicData
from app.telegram.filters.states import SGBuyStars
from app.telegram.keyboards.callback_data.menu import CDTelegramStars
from app.telegram.keyboards.callback_data.purchase import CDConfirmPurchase, CDSelectUsername
from app.telegram.keyboards.menu import to_menu_keyboard
from app.telegram.keyboards.purchase import confirm_purchase_keyboard, enter_username_keyboard
from app.telegram.middlewares import TonConnectCheckerMiddleware

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.services.backend import Backend
    from app.services.backend.types import Recipient, Transaction
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)
TonConnectCheckerMiddleware().setup_inner(router)


@router.callback_query(CDTelegramStars.filter())
async def proceed_stars_purchase(
    query: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
) -> Any:
    await state.set_state(SGBuyStars.enter_username)
    message: Message = await helper.answer(  # type: ignore[assignment]
        text=i18n.messages.purchase.enter_username(),
        reply_markup=enter_username_keyboard(i18n=i18n, username=query.from_user.username),
    )
    await state.set_data({"message_id": message.message_id})


@router.message(SGBuyStars.enter_username, F.text.as_("username"))
@router.callback_query(
    SGBuyStars.enter_username,
    CDSelectUsername.filter(),
    MagicData(F.callback_data.username.as_("username")),
)
async def save_stars_recipient(
    _: Message,
    helper: MessageHelper,
    username: str,
    i18n: I18nContext,
    backend: Backend,
) -> Any:
    recipient: Recipient = await backend.resolve_stars_recipient(username=username)
    await helper.next_step(
        state=SGBuyStars.enter_count,
        text=i18n.messages.purchase.enter_count(),
        reply_markup=to_menu_keyboard(i18n=i18n),
        update={"username": username, "recipient": recipient.recipient},
    )


@router.message(SGBuyStars.enter_count, F.text.cast(int).as_("quantity"))
async def save_stars_count(
    _: Message,
    helper: MessageHelper,
    state: FSMContext,
    quantity: int,
    i18n: I18nContext,
    backend: Backend,
    assets: Assets,
) -> Any:
    if quantity < assets.shop.min_stars or quantity > assets.shop.max_stars:
        return await helper.edit_current_message(
            text=i18n.messages.purchase.wrong_count(
                minimum=assets.shop.min_stars,
                maximum=assets.shop.max_stars,
                entered=quantity,
            ),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
    data: dict[str, Any] = await state.get_data()
    price: PriceDto = await get_stars_price(quantity=quantity, backend=backend, assets=assets)
    await helper.next_step(
        state=SGBuyStars.confirm,
        text=i18n.messages.purchase.confirm(
            username=data["username"].removeprefix("@"),
            product=i18n.messages.purchase.stars(count=quantity),
            usd_price=price.usd_price,
            ton_price=price.ton_price,
        ),
        reply_markup=confirm_purchase_keyboard(i18n=i18n),
        update={"quantity": quantity},
    )


@router.callback_query(SGBuyStars.confirm, CDConfirmPurchase.filter())
async def buy_stars(
    _: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    ton_connect: TcAdapter,
    backend: Backend,
) -> Any:
    data: dict[str, Any] = await state.get_data()
    transaction: Transaction = await backend.buy_stars(
        recipient=data["recipient"],
        quantity=data["quantity"],
        username=data["username"],
    )
    await state.clear()
    await helper.answer(
        text=i18n.messages.confirm_transaction(),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )
    try:
        await ton_connect.send_transaction(transaction)
    except UserRejectsError:
        await helper.answer(
            text=i18n.messages.transaction_canceled(),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
