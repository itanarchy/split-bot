from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.dto import UserDto

from .base import Base, Int64
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[Int64] = mapped_column(nullable=False, unique=True)
    backend_user_id: Mapped[Optional[Int64]] = mapped_column(nullable=True, unique=True)
    backend_access_token: Mapped[Optional[str]] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=False)
    wallet_address: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    locale: Mapped[str] = mapped_column(String(length=2), nullable=False)
    bot_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)
    inviter: Mapped[Optional[str]] = mapped_column(nullable=True)

    def dto(self) -> UserDto:
        return UserDto.model_validate(self)
