from typing import Optional
from uuid import UUID

from app.enums import DeepLinkAction
from app.models.base import PydanticModel


class DeepLinkDto(PydanticModel):
    id: UUID
    owner_id: int
    action: DeepLinkAction
    gift_code_address: Optional[str] = None
    gift_code_seed: Optional[str] = None
