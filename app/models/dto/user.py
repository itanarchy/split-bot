from typing import Optional

from aiogram import html
from aiogram.utils.link import create_tg_link

from app.models.base import PydanticModel


class UserDto(PydanticModel):
    id: int
    telegram_id: int
    backend_user_id: Optional[int] = None
    backend_access_token: Optional[str] = None
    name: str
    wallet_address: Optional[str] = None
    locale: str
    bot_blocked: bool = False
    inviter: Optional[str] = None

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.telegram_id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)

    @property
    def wallet_connected(self) -> bool:
        return self.wallet_address is not None
