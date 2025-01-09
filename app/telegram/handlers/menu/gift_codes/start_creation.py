from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from app.enums import GiftCodeCreationStatus
from app.models.dto import GiftCodeCreation
from app.services.backend import Backend
from app.telegram.filters.states import NoneState, SGCreateGiftCode
from app.telegram.keyboards.callback_data.gift_codes import CDCreateGiftCode
from app.telegram.keyboards.callback_data.menu import CDRefresh
from app.telegram.keyboards.gift_codes import gift_code_creation_keyboard
from app.utils.localization.patches import FluentNullable

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


async def show_gift_code_creation(
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    backend: Backend,
    assets: Assets,
    gift_code_creation: Optional[GiftCodeCreation] = None,
    **kwargs: Any,
) -> Any:
    await state.set_state(SGCreateGiftCode.waiting)
    if gift_code_creation is None:
        gift_code_creation = await GiftCodeCreation.from_state(state=state)
    for key, value in kwargs.items():
        setattr(gift_code_creation, key, value)
    status: GiftCodeCreationStatus = gift_code_creation.status(assets=assets)
    ton_rate: Optional[float] = None
    if gift_code_creation.amount is not None:
        ton_rate = await backend.get_ton_rate()

    answer, fsm_data = await helper.edit_current_message(
        text=i18n.messages.gift_codes.info(
            activations=FluentNullable(gift_code_creation.activations),
            amount=FluentNullable(gift_code_creation.amount),
            usd_amount=FluentNullable(gift_code_creation.usd_amount(ton_rate=ton_rate)),
            min_activations=assets.gift_codes.min_activations,
            max_activations=assets.gift_codes.max_activations,
            min_amount=assets.gift_codes.min_amount,
            max_amount=assets.gift_codes.max_amount,
            status=status,
        ),
        reply_markup=gift_code_creation_keyboard(i18n=i18n, status=status),
    )

    old_message_id: Optional[int] = gift_code_creation.message_id
    new_message_id: Optional[int] = fsm_data.get("message_id")
    if new_message_id is not None and old_message_id != new_message_id:
        gift_code_creation.message_id = new_message_id
    gift_code_creation.to_delete.clear()
    await gift_code_creation.update_state(state=state)


@router.callback_query(NoneState, CDCreateGiftCode.filter())
@router.callback_query(SGCreateGiftCode(), CDRefresh.filter())
async def start_gift_code_creation(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    backend: Backend,
    assets: Assets,
    raw_state: Optional[str] = None,
) -> Any:
    await show_gift_code_creation(
        helper=helper,
        i18n=i18n,
        state=state,
        backend=backend,
        assets=assets,
        gift_code_creation=GiftCodeCreation() if raw_state is None else None,
    )
