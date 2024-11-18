from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import UserRejectsError

from app.services.backend.errors import SplitBadRequestError
from app.telegram.filters.states import SGBuyStars
from app.telegram.keyboards.callback_data.menu import CDTelegramStars
from app.telegram.keyboards.callback_data.purchase import CDConfirmPurchase
from app.telegram.keyboards.menu import to_menu_keyboard
from app.telegram.keyboards.purchase import confirm_purchase_keyboard
from app.telegram.middlewares import TonConnectCheckerMiddleware

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.models.dto import UserDto
    from app.services.backend import Backend
    from app.services.backend.types import Recipient, Transaction
    from app.services.ton_connect import TcAdapter
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)
TonConnectCheckerMiddleware().setup_inner(router)


@router.callback_query(CDTelegramStars.filter())
async def proceed_stars_purchase(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
) -> Any:
    await state.set_state(SGBuyStars.enter_username)
    message: Message = await helper.answer(  # type: ignore[assignment]
        text=i18n.messages.purchase.enter_username(),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )
    await state.set_data({"message_id": message.message_id})


@router.message(SGBuyStars.enter_username, F.text.as_("username"))
async def save_username(
    _: Message,
    helper: MessageHelper,
    username: str,
    i18n: I18nContext,
    user: UserDto,
    backend: Backend,
) -> Any:
    try:
        recipient: Recipient = await backend.resolve_stars_recipient(
            access_token=user.backend_access_token,
            username=username,
        )
    except SplitBadRequestError as error:
        return await helper.edit_current_message(
            text=error.message,
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
    await helper.next_step(
        state=SGBuyStars.enter_count,
        text=i18n.messages.purchase.enter_count(),
        reply_markup=to_menu_keyboard(i18n=i18n),
        update={"username": username, "recipient": recipient.recipient},
    )


@router.message(SGBuyStars.enter_count, F.text.cast(int).as_("count"))
async def save_stars_count(
    _: Message,
    helper: MessageHelper,
    state: FSMContext,
    count: int,
    i18n: I18nContext,
    assets: Assets,
) -> Any:
    if count < assets.shop.min_stars or count > assets.shop.max_stars:
        return await helper.edit_current_message(
            text=i18n.messages.purchase.wrong_count(
                minimum=assets.shop.min_stars,
                maximum=assets.shop.max_stars,
                entered=count,
            ),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
    data: dict[str, Any] = await state.get_data()
    await helper.next_step(
        state=SGBuyStars.confirm,
        text=i18n.messages.purchase.confirm(
            username=data["username"],
            product=i18n.messages.purchase.stars(count=count),
            price=count * assets.shop.stars_price,
        ),
        reply_markup=confirm_purchase_keyboard(i18n=i18n),
        update={"quantity": count},
    )


@router.callback_query(SGBuyStars.confirm, CDConfirmPurchase.filter())
async def buy_stars(
    _: CallbackQuery,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    ton_connect: TcAdapter,
    user: UserDto,
    backend: Backend,
) -> Any:
    data: dict[str, Any] = await state.get_data()
    try:
        transaction: Transaction = await backend.buy_stars(
            access_token=user.backend_access_token,
            recipient=data["recipient"],
            quantity=data["quantity"],
        )
    except SplitBadRequestError as error:
        return await helper.edit_current_message(
            text=error.message,
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
    await state.clear()
    await helper.answer(
        text=i18n.messages.confirm_transaction(),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )
    try:
        await ton_connect.send_transaction(transaction)
    except UserRejectsError:
        await helper.answer(text=i18n.messages.transaction_canceled())
