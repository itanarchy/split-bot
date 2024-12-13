from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    TelegramObject,
)
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.link import create_telegram_link
from aiogram_i18n import I18nContext

from app.telegram.keyboards.callback_data.menu import CDReferralProgram
from app.telegram.keyboards.menu import menu_keyboard
from app.telegram.keyboards.referral import join_bot_keyboard, referral_program_keyboard

if TYPE_CHECKING:
    from app.models.dto import UserDto
    from app.telegram.helpers.messages import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.callback_query(CDReferralProgram.filter())
async def show_referral_link(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    bot: Bot,
    user: UserDto,
) -> Any:
    if user.wallet_address is None:
        return await helper.answer(
            text=i18n.messages.wallet_not_connected(),
            reply_markup=menu_keyboard(i18n=i18n, wallet_connected=user.wallet_connected),
        )

    url: str = await create_start_link(bot=bot, payload=user.wallet_address)
    return await helper.answer(
        text=i18n.messages.referral.info(link=url),
        reply_markup=referral_program_keyboard(i18n=i18n, url=url),
    )


@router.inline_query()
async def show_inline_query_menu(
    query: InlineQuery,
    i18n: I18nContext,
    bot: Bot,
    user: UserDto,
) -> Any:
    results: list[InlineQueryResultArticle] = []
    if user.wallet_connected:
        url: str = await create_start_link(bot=bot, payload=user.wallet_address)
        invite_text: str = i18n.messages.referral.invite(link=url)
        results.append(
            InlineQueryResultArticle(
                id=user.wallet_address,
                title=i18n.buttons.share(),
                input_message_content=InputTextMessageContent(message_text=invite_text),
            )
        )
    else:
        url = create_telegram_link((await bot.me()).username)
        results.append(
            InlineQueryResultArticle(
                id="null",
                title=i18n.messages.wallet_not_connected(),
                input_message_content=InputTextMessageContent(message_text=r"¯\_(ツ)_/¯"),
                reply_markup=join_bot_keyboard(i18n=i18n, url=url),
            )
        )

    return await query.answer(results=results, cache_time=0)  # type: ignore
