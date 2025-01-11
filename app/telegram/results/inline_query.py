from typing import cast

from aiogram import Bot
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.link import create_telegram_link
from aiogram_i18n import I18nContext

from app.telegram.keyboards.referral import join_bot_keyboard


async def not_found_answer(title: str, i18n: I18nContext, bot: Bot) -> InlineQueryResultArticle:
    username: str = cast(str, (await bot.me()).username)
    return InlineQueryResultArticle(
        id="null",
        title=title,
        input_message_content=InputTextMessageContent(message_text=r"¯\_(ツ)_/¯"),
        reply_markup=join_bot_keyboard(i18n=i18n, url=create_telegram_link(username)),
    )
