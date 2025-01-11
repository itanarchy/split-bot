from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final, Optional
from uuid import UUID

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.deep_linking import create_start_link
from aiogram_i18n import I18nContext
from tonutils.client import ToncenterClient

from app.controllers.gift_codes.get import get_giftcode_data
from app.telegram.keyboards.gift_codes import claim_gift_code_keyboard
from app.telegram.results.inline_query import not_found_answer

if TYPE_CHECKING:
    from app.models.dto import DeepLinkDto, FullGiftCodeData
    from app.services.deep_links import DeepLinksService

router: Final[Router] = Router(name=__name__)


@router.inline_query(F.query.cast(UUID).as_("link_id"))
async def show_deep_link(
    query: InlineQuery,
    link_id: UUID,
    i18n: I18nContext,
    bot: Bot,
    toncenter: ToncenterClient,
    deep_links: DeepLinksService,
) -> Any:
    deep_link: Optional[DeepLinkDto] = await deep_links.get(link_id=link_id)
    if deep_link is None:
        return UNHANDLED

    try:
        giftcode_data: FullGiftCodeData = await get_giftcode_data(
            address=deep_link.gift_code_address,
            toncenter=toncenter,
        )
    except ValueError:
        return query.answer(
            results=[
                await not_found_answer(
                    title=i18n.messages.gift_codes.not_found(),
                    i18n=i18n,
                    bot=bot,
                )
            ],
            cache_time=0,
        )

    if giftcode_data.fully_activated:
        return query.answer(
            results=[
                await not_found_answer(
                    title=i18n.messages.gift_codes.expired(),
                    i18n=i18n,
                    bot=bot,
                )
            ],
            cache_time=0,
        )

    share_text: str = i18n.messages.gift_codes.shared(
        total_amount=giftcode_data.total_amount,
        amount=giftcode_data.max_buy_amount,
        activations_left=giftcode_data.activations_left,
        max_activations=giftcode_data.max_activations,
    )
    url: str = await create_start_link(bot=bot, payload=deep_link.id.hex)
    return query.answer(
        results=[
            InlineQueryResultArticle(
                id=deep_link.id.hex,
                title=i18n.buttons.share_gift_code(),
                input_message_content=InputTextMessageContent(message_text=share_text),
                reply_markup=claim_gift_code_keyboard(i18n=i18n, url=url),
            ),
        ],
        cache_time=0,
    )
