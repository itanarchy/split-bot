from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from aiogram.utils.deep_linking import create_start_link
from aiogram_i18n import I18nContext
from pytonconnect.exceptions import UserRejectsError

from app.enums import DeepLinkAction, GiftCodeCreationStatus
from app.models.dto import DeepLinkDto, GiftCodeCreation, UserDto
from app.services.backend import Backend
from app.services.backend.types import NewGiftCode
from app.services.deep_links import DeepLinksService
from app.services.ton_connect import TcAdapter
from app.telegram.filters.states import SGCreateGiftCode
from app.telegram.handlers.menu.gift_codes.start_creation import show_gift_code_creation
from app.telegram.keyboards.callback_data.gift_codes import CDConfirmGiftCode
from app.telegram.keyboards.menu import to_menu_keyboard
from app.telegram.keyboards.referral import share_keyboard

if TYPE_CHECKING:
    from app.models.config import Assets
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.callback_query(SGCreateGiftCode.waiting, CDConfirmGiftCode.filter())
async def create_gift_code(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    state: FSMContext,
    bot: Bot,
    ton_connect: TcAdapter,
    backend: Backend,
    deep_links: DeepLinksService,
    user: UserDto,
    assets: Assets,
) -> None:
    gift_code_creation: GiftCodeCreation = await GiftCodeCreation.from_state(state=state)
    if gift_code_creation.status(assets=assets) != GiftCodeCreationStatus.READY:
        return await show_gift_code_creation(
            helper=helper,
            i18n=i18n,
            state=state,
            backend=backend,
            assets=assets,
        )

    gift_code: NewGiftCode = await backend.create_gift_code(
        max_activations=gift_code_creation.activations,
        max_buy_amount=gift_code_creation.amount,
    )

    await state.clear()
    await helper.answer(
        text=i18n.messages.confirm_transaction(),
        reply_markup=to_menu_keyboard(i18n=i18n),
    )

    deep_link: DeepLinkDto = await deep_links.create(
        owner_id=user.id,
        action=DeepLinkAction.USE_GIFT_CODE,
        gift_code_address=gift_code.address,
        gift_code_seed=gift_code.seed,
    )
    url: str = await create_start_link(bot=bot, payload=deep_link.id.hex)
    await helper.answer(
        text=i18n.messages.gift_codes.created(link=url),
        reply_markup=share_keyboard(i18n=i18n, deep_link_id=deep_link.id.hex),
        edit=False,
        delete=False,
    )

    try:
        await ton_connect.send_transaction(gift_code.transaction)
    except UserRejectsError:
        await helper.answer(
            text=i18n.messages.transaction_canceled(),
            reply_markup=to_menu_keyboard(i18n=i18n),
        )
