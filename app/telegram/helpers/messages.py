from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, cast

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import (
    CallbackQuery,
    InaccessibleMessage,
    InlineKeyboardMarkup,
    Message,
    ReplyParameters,
)
from aiogram_i18n import I18nContext

from app.types import AnyKeyboard
from app.utils.time import datetime_now

from .exceptions import silent_bot_request


@dataclass(kw_only=True)
class MessageHelper:
    update: Optional[Message | CallbackQuery] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    bot: Bot
    fsm: FSMContext
    i18n: I18nContext
    last_updated: datetime = field(default_factory=datetime_now)

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

    def resolve_message_id(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> tuple[int, Optional[int], bool]:
        chat_id = chat_id or self.chat_id
        message_id = message_id or self.message_id
        can_be_edited: bool = True
        if isinstance(self.update, Message):
            chat_id = chat_id or self.update.chat.id
            message_id = message_id or self.update.message_id
            can_be_edited = self.update.from_user.id == self.bot.id  # type: ignore
        elif isinstance(self.update, CallbackQuery):
            if self.update.message is None:
                raise RuntimeError("Message is unavailable.")
            if chat_id is None:
                chat_id = self.update.message.chat.id
            if message_id is None:
                message_id = self.update.message.message_id
            if isinstance(self.update.message, InaccessibleMessage):
                can_be_edited = False
        if chat_id is None:
            raise RuntimeError("Chat is unavailable.")
        return chat_id, message_id, can_be_edited

    def get_chat_id(self) -> int:
        return self.resolve_message_id()[0]

    def find_message_id(self) -> Optional[int]:
        return self.resolve_message_id()[1]

    async def get_message_id(self) -> Optional[int]:
        return (await self.fsm.get_data()).get("message_id")

    async def delete(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
    ) -> bool:
        chat_id, message_id, *_ = self.resolve_message_id(chat_id=chat_id, message_id=message_id)
        if message_id is not None:
            with silent_bot_request():
                await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
                return True
        return False

    async def delete_many(
        self,
        chat_id: Optional[int] = None,
        message_ids: Optional[list[int]] = None,
    ) -> None:
        if not message_ids:
            return
        chat_id, *_ = self.resolve_message_id(chat_id=chat_id, message_id=message_ids[0])
        with silent_bot_request():
            await self.bot.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
            )

    async def send_new_message(
        self,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[AnyKeyboard] = None,
        delete: bool = True,
        **kwargs: Any,
    ) -> Message:
        chat_id, message_id, *_ = self.resolve_message_id(
            chat_id=chat_id,
            message_id=message_id,
        )
        if delete:
            await self.delete(chat_id=chat_id, message_id=message_id)
        return await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            **kwargs,
        )

    async def answer(
        self,
        *,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        edit: bool = True,
        reply: bool = False,
        delete: bool = False,
        force_edit: bool = False,
        **kwargs: Any,
    ) -> bool | Message:
        chat_id, message_id, can_be_edited = self.resolve_message_id(
            chat_id=chat_id, message_id=message_id
        )
        if force_edit or (edit and can_be_edited and message_id):
            try:
                return await self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    reply_markup=reply_markup,
                    **kwargs,
                )
            except (TelegramBadRequest, TelegramForbiddenError) as error:
                if "exactly the same as a current content" in str(error):
                    return True
            finally:
                self.last_updated = datetime_now()

        message_id = cast(int, message_id)
        if reply and isinstance(self.update, Message):
            kwargs["reply_parameters"] = ReplyParameters(message_id=message_id)
        try:
            return await self.send_new_message(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                delete=delete,
                **kwargs,
            )
        finally:
            self.last_updated = datetime_now()

    async def edit_current_message(
        self,
        *,
        message_id: Optional[int] = None,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        fsm_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> tuple[Message | bool, dict[str, Any]]:
        if fsm_data is None:
            fsm_data = await self.fsm.get_data()

        if isinstance(self.update, CallbackQuery):
            message: Message = cast(Message, self.update.message)
        else:
            message = cast(Message, self.update)
            with silent_bot_request():
                await message.delete()

        to_delete: list[int] = fsm_data.setdefault("to_delete", [])
        if message_id is None:
            message_id = fsm_data.setdefault("message_id", message.message_id)
        await self.delete_many(chat_id=message.chat.id, message_ids=to_delete)
        new_message: bool | Message = await self.answer(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            force_edit=True,
            **kwargs,
        )

        fsm_data["message_id"] = (
            new_message.message_id if isinstance(new_message, Message) else message_id
        )
        await self.fsm.set_data(fsm_data)

        return new_message, fsm_data

    async def next_step(
        self,
        *,
        state: State,
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        update: Optional[dict[str, Any]] = None,
        **extra: Any,
    ) -> bool | Message:
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
