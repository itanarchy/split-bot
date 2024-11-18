from __future__ import annotations

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64
from .mixins.timestamp import TimestampMixin


class TcRecord(Base, TimestampMixin):
    __tablename__ = "tc_records"
    __table_args__ = (
        Index(
            "uix_telegram_id_key",
            "telegram_id",
            "key",
            unique=True,
            postgresql_include=["value"],
        ),
    )

    id: Mapped[Int64] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[Int64] = mapped_column(nullable=False)
    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
