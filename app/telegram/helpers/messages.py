from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Union, cast

from aiogram import Bot
from aiogram.client.default import Default
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import (
    CallbackQuery,
    InaccessibleMessage,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    Message,
    MessageEntity,
)
from aiogram_i18n import I18nContext

from ...types import AnyKeyboard
from .exceptions import silent_bot_request


@dataclass(kw_only=True)
class MessageHelper:
    update: Optional[Message | CallbackQuery] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    bot: Bot
    fsm: FSMContext
    i18n: I18nContext

    def copy(
        self,
        *,
        update: Optional[Message | CallbackQuery] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> MessageHelper:
        return MessageHelper(
            update=update or self.update,
            chat_id=chat_id or self.chat_id,
            message_id=message_id or self.message_id,
            bot=self.bot,
            fsm=self.fsm,
            i18n=self.i18n,
        )

    def _resolve_query_message(self) -> tuple[int, Optional[int], bool]:
        callback_query: Optional[CallbackQuery] = cast(Optional[CallbackQuery], self.update)
        chat_id: Optional[int] = self.chat_id
        message_id: Optional[int] = self.message_id
        can_be_edited: bool = True
        if callback_query is not None:
            if callback_query.message is None:
                raise RuntimeError("Message is unavailable.")
            if chat_id is None:
                chat_id = callback_query.message.chat.id
            if message_id is None:
                message_id = callback_query.message.message_id
            if isinstance(callback_query.message, InaccessibleMessage):
                can_be_edited = False
        if chat_id is None:
            raise RuntimeError("Chat is unavailable.")
        return chat_id, message_id, can_be_edited

    async def send_new_message(
        self,
        *,
        text: str,
        parse_mode: Optional[Union[str, Default]] = Default("parse_mode"),
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[AnyKeyboard] = None,
        disable_web_page_preview: Optional[bool | Default] = Default("link_preview_is_disabled"),
        request_timeout: Optional[int] = None,
        delete: bool = True,
        **kwargs: Any,
    ) -> Message:
        chat_id, message_id, *_ = self._resolve_query_message()
        if delete and message_id is not None:
            with silent_bot_request():
                await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
        return await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            request_timeout=request_timeout,
            **kwargs,
        )

    async def answer(
        self,
        *,
        text: str,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[Union[str, Default]] = Default("parse_mode"),
        entities: Optional[list[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        disable_web_page_preview: Optional[bool | Default] = Default("link_preview_is_disabled"),
        request_timeout: Optional[int] = None,
        edit: bool = True,
        reply: bool = False,
        delete: bool = True,
        **kwargs: Any,
    ) -> bool | Message:
        if isinstance(self.update, Message):
            if reply:
                kwargs["reply_to_message_id"] = self.update.message_id
            return await self.bot.send_message(
                chat_id=self.chat_id or self.update.chat.id,
                text=text,
                parse_mode=parse_mode,
                entities=entities,
                link_preview_options=link_preview_options,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview,
                request_timeout=request_timeout,
                **kwargs,
            )
        if edit:
            with silent_bot_request():
                chat_id, message_id, can_be_edited = self._resolve_query_message()
                if message_id is not None and can_be_edited:
                    return await self.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text,
                        inline_message_id=inline_message_id,
                        parse_mode=parse_mode,
                        entities=entities,
                        link_preview_options=link_preview_options,
                        reply_markup=reply_markup,
                        disable_web_page_preview=disable_web_page_preview,
                        request_timeout=request_timeout,
                    )
        return await self.send_new_message(
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview,
            request_timeout=request_timeout,
            delete=delete,
            **kwargs,
        )

    async def edit_current_message(
        self,
        *,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        **kwargs: Any,
    ) -> tuple[Message, dict[str, Any]]:
        if isinstance(self.update, CallbackQuery):
            message: Message = cast(Message, self.update.message)
        else:
            message = cast(Message, self.update)
            with silent_bot_request():
                await message.delete()

        data: dict[str, Any] = await self.fsm.get_data()
        return (
            cast(
                Message,
                await self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=data["message_id"],
                    text=text,
                    reply_markup=reply_markup,
                    **kwargs,
                ),
            ),
            data,
        )

    async def next_step(
        self,
        *,
        state: State,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        update: Optional[dict[str, Any]] = None,
        **extra: Any,
    ) -> Message:
        result, data = await self.edit_current_message(
            text=text,
            reply_markup=reply_markup,
            **extra,
        )
        if update is not None:
            data.update(update)
            await self.fsm.set_data(data)
        await self.fsm.set_state(state)
        return result
