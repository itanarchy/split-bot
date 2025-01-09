from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, TelegramObject
from aiogram_i18n import I18nContext

from app.models.dto import GiftCodeCreation
from app.services.backend import Backend
from app.telegram.filters.states import SGCreateGiftCode
from app.telegram.handlers.menu.gift_codes.start_creation import show_gift_code_creation
from app.telegram.keyboards.callback_data.gift_codes import (
    CDSetGiftCodeActivations,
    CDSetGiftCodeAmount,
)
from app.telegram.keyboards.callback_data.menu import CDRefresh
from app.telegram.keyboards.menu import cancel_keyboard

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.callback_query(SGCreateGiftCode(), CDSetGiftCodeAmount.filter())
async def ask_gift_code_amount(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    assets: Assets,
) -> Any:
    gift_code_creation: GiftCodeCreation = await GiftCodeCreation.from_state(state=state)
    message: Message = await helper.answer(  # type: ignore
        text=i18n.messages.gift_codes.enter_amount(
            min=assets.gift_codes.min_amount,
            max=assets.gift_codes.max_amount,
        ),
        reply_markup=cancel_keyboard(i18n=i18n, data=CDRefresh()),
        edit=False,
        delete=False,
    )
    gift_code_creation.to_delete.append(message.message_id)
    await state.set_state(SGCreateGiftCode.amount)
    await gift_code_creation.update_state(state=state)


@router.callback_query(SGCreateGiftCode(), CDSetGiftCodeActivations.filter())
async def ask_gift_code_activations(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    assets: Assets,
) -> Any:
    gift_code_creation: GiftCodeCreation = await GiftCodeCreation.from_state(state=state)
    message: Message = await helper.answer(  # type: ignore
        text=i18n.messages.gift_codes.enter_activations(
            min=assets.gift_codes.min_activations,
            max=assets.gift_codes.max_activations,
        ),
        reply_markup=cancel_keyboard(i18n=i18n, data=CDRefresh()),
        edit=False,
        delete=False,
    )
    gift_code_creation.to_delete.append(message.message_id)
    await state.set_state(SGCreateGiftCode.activations)
    await gift_code_creation.update_state(state=state)


@router.message(SGCreateGiftCode.amount, F.text.cast(float).as_("amount"))
async def set_gift_code_amount(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    backend: Backend,
    assets: Assets,
    amount: float,
) -> Any:
    await show_gift_code_creation(
        helper=helper,
        i18n=i18n,
        state=state,
        backend=backend,
        assets=assets,
        amount=amount,
    )


@router.message(SGCreateGiftCode.activations, F.text.cast(int).as_("activations"))
async def set_gift_code_activations(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    backend: Backend,
    assets: Assets,
    activations: int,
) -> Any:
    await show_gift_code_creation(
        helper=helper,
        i18n=i18n,
        state=state,
        backend=backend,
        assets=assets,
        activations=activations,
    )
