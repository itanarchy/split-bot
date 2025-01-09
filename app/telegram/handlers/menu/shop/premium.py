from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import UserRejectsError

from app.controllers.price import PriceDto, get_premium_price
from app.telegram.filters import MagicData
from app.telegram.filters.states import SGBuyPremium
from app.telegram.keyboards.callback_data.menu import CDTelegramPremium
from app.telegram.keyboards.callback_data.purchase import (
    CDConfirmPurchase,
    CDSelectSubscriptionPeriod,
    CDSelectUsername,
)
from app.telegram.keyboards.menu import to_menu_keyboard
from app.telegram.keyboards.purchase import (
    confirm_purchase_keyboard,
    enter_username_keyboard,
    subscription_period_keyboard,
)
from app.telegram.middlewares import TonConnectCheckerMiddleware

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.services.backend import Backend
    from app.services.backend.types import Recipient, Transaction
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)
TonConnectCheckerMiddleware().setup_inner(router)


@router.callback_query(CDTelegramPremium.filter())
async def proceed_premium_purchase(
    query: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
) -> Any:
    await state.set_state(SGBuyPremium.enter_username)
    message: Message = await helper.answer(  # type: ignore[assignment]
        text=i18n.messages.purchase.enter_username(),
        reply_markup=enter_username_keyboard(i18n=i18n, username=query.from_user.username),
    )
    await state.set_data({"message_id": message.message_id})


@router.message(SGBuyPremium.enter_username, F.text.as_("username"))
@router.callback_query(
    SGBuyPremium.enter_username,
    CDSelectUsername.filter(),
    MagicData(F.callback_data.username.as_("username")),
)
async def save_premium_recipient(
    _: TelegramObject,
    helper: MessageHelper,
    username: str,
    i18n: I18nContext,
    backend: Backend,
    assets: Assets,
) -> Any:
    recipient: Recipient = await backend.resolve_premium_recipient(username=username)
    await helper.next_step(
        state=SGBuyPremium.select_period,
        text=i18n.messages.purchase.select_period(),
        reply_markup=subscription_period_keyboard(i18n=i18n, assets=assets),
        update={"username": username, "recipient": recipient.recipient},
    )


@router.callback_query(
    SGBuyPremium.select_period,
    CDSelectSubscriptionPeriod.filter(),
    MagicData(F.callback_data.period.as_("period")),
)
@flags.callback_query(disabled=True)
async def save_subscription_period(
    query: CallbackQuery,
    helper: MessageHelper,
    state: FSMContext,
    period: int,
    i18n: I18nContext,
    backend: Backend,
    assets: Assets,
) -> Any:
    if period not in assets.shop.subscription_periods:
        await query.answer(text=i18n.messages.purchase.subscription_not_available())
        return await helper.answer(
            text=i18n.messages.purchase.select_period(),
            reply_markup=subscription_period_keyboard(i18n=i18n, assets=assets),
        )

    price: PriceDto = await get_premium_price(months=period, backend=backend, assets=assets)
    await query.answer()
    data: dict[str, Any] = await state.get_data()
    await helper.next_step(
        state=SGBuyPremium.confirm,
        text=i18n.messages.purchase.confirm(
            username=data["username"].removeprefix("@"),
            product=i18n.messages.purchase.premium(period=period),
            usd_price=price.usd_price,
            ton_price=price.ton_price,
        ),
        reply_markup=confirm_purchase_keyboard(i18n=i18n),
        update={"period": period},
    )


@router.callback_query(SGBuyPremium.confirm, CDConfirmPurchase.filter())
async def buy_premium(
    _: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    ton_connect: TcAdapter,
    backend: Backend,
) -> Any:
    data: dict[str, Any] = await state.get_data()
    transaction: Transaction = await backend.buy_premium(
        recipient=data["recipient"],
        months=data["period"],
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
