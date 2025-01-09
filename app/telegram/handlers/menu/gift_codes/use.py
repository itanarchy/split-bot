from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional
from uuid import UUID

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import UserRejectsError
from tonutils.client import ToncenterClient

from app.controllers.gift_codes.get import get_giftcode_data
from app.enums import DeepLinkAction
from app.models.dto import DeepLinkDto, FullGiftCodeData, GiftCodeActivation, UserDto
from app.services.backend import Backend
from app.services.backend.types import Recipient, Transaction
from app.services.deep_links import DeepLinksService
from app.services.ton_connect import TcAdapter
from app.telegram.filters import MagicData
from app.telegram.filters.states import SGUseGiftCode
from app.telegram.handlers.menu.main import show_main_menu
from app.telegram.keyboards.callback_data.gift_codes import CDUseGiftCode
from app.telegram.keyboards.callback_data.purchase import CDSelectUsername
from app.telegram.keyboards.menu import back_keyboard, to_menu_keyboard
from app.telegram.keyboards.purchase import enter_username_keyboard
from app.telegram.keyboards.ton_connect import connect_wallet_keyboard

if TYPE_CHECKING:
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(magic=F.args.cast(UUID).as_("link_id")))
@router.callback_query(
    CDUseGiftCode.filter(),
    MagicData(F.callback_data.link_id.as_("link_id")),
)
async def search_gift_code(
    _: TelegramObject,
    link_id: UUID,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    event_from_user: AiogramUser,
    toncenter: ToncenterClient,
    deep_links: DeepLinksService,
    user: UserDto,
) -> Any:
    deep_link: Optional[DeepLinkDto] = await deep_links.get(link_id=link_id)
    if deep_link is None or deep_link.action != DeepLinkAction.USE_GIFT_CODE:
        return await show_main_menu(
            _=_,
            helper=helper,
            i18n=i18n,
            state=state,
            user=user,
        )

    giftcode_data: FullGiftCodeData = await get_giftcode_data(
        address=deep_link.gift_code_address,
        toncenter=toncenter,
    )

    if giftcode_data.activations_left <= 0:
        return await helper.answer(
            text=i18n.messages.gift_codes.expired(),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )

    if user.wallet_address is None:
        return await helper.answer(
            text=i18n.messages.wallet_not_connected(),
            reply_markup=connect_wallet_keyboard(i18n=i18n),
        )

    message: Message = await helper.answer(  # type: ignore
        text=i18n.messages.gift_codes.view(
            max_buy_amount=giftcode_data.max_buy_amount,
            activations_left=giftcode_data.activations_left,
            max_activations=giftcode_data.max_activations,
        ),
        reply_markup=enter_username_keyboard(i18n=i18n, username=event_from_user.username),
    )

    activation: GiftCodeActivation = GiftCodeActivation(
        link_id=deep_link.id,
        contract_address=deep_link.gift_code_address,
        seed=deep_link.gift_code_seed,
        message_id=message.message_id,
    )
    await state.set_state(SGUseGiftCode.username)
    await activation.update_state(state=state)


@router.message(SGUseGiftCode.username, F.text.as_("username"))
@router.callback_query(
    SGUseGiftCode.username,
    CDSelectUsername.filter(),
    MagicData(F.callback_data.username.as_("username")),
)
async def use_gift_code(
    _: TelegramObject,
    helper: MessageHelper,
    username: str,
    i18n: I18nContext,
    state: FSMContext,
    toncenter: ToncenterClient,
    ton_connect: TcAdapter,
    backend: Backend,
) -> Any:
    activation: GiftCodeActivation = await GiftCodeActivation.from_state(state=state)
    recipient: Recipient = await backend.resolve_stars_recipient(username=username)
    giftcode_data: FullGiftCodeData = await get_giftcode_data(
        address=activation.contract_address,
        toncenter=toncenter,
    )

    if giftcode_data.activations_left <= 0:
        return await helper.edit_current_message(
            text=i18n.messages.gift_codes.expired(),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )

    await state.set_state()
    transaction: Transaction = await backend.use_gift_code(
        seed=activation.seed,
        amount=giftcode_data.max_buy_amount,
        recipient=recipient.recipient,
        gift_code_address=activation.contract_address,
        owner_address=giftcode_data.owner_address,
    )

    text: str = i18n.messages.gift_codes.use_requested(username=username.removeprefix("@"))
    await helper.edit_current_message(
        text=text,
        reply_markup=back_keyboard(i18n=i18n, data=CDUseGiftCode(link_id=activation.link_id)),
    )

    try:
        await ton_connect.send_transaction(transaction)
    except UserRejectsError:
        await helper.edit_current_message(
            text=i18n.messages.transaction_canceled(),
            reply_markup=to_menu_keyboard(i18n=i18n),
            delete=False,
        )
