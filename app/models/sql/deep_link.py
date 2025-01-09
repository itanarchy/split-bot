from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.enums import DeepLinkAction
from app.models.dto import DeepLinkDto
from app.utils.custom_types import Int64

from .base import Base
from .mixins import TimestampMixin


class DeepLink(Base, TimestampMixin):
    __tablename__ = "deep_links"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    owner_id: Mapped[Int64] = mapped_column(ForeignKey("users.id"))
    action: Mapped[DeepLinkAction] = mapped_column(default=DeepLinkAction.INVITE)
    gift_code_address: Mapped[Optional[str]] = mapped_column(nullable=True)
    gift_code_seed: Mapped[Optional[str]] = mapped_column(nullable=True)

    def dto(self) -> DeepLinkDto:
        return DeepLinkDto.model_validate(self)
