from typing import Optional
from uuid import UUID

from pydantic import Field

from app.enums import GiftCodeCreationStatus
from app.models.base import PydanticModel
from app.models.config import Assets


class GiftCodeCreation(PydanticModel):
    activations: Optional[int] = None
    amount: Optional[float] = None
    message_id: Optional[int] = None
    to_delete: list[int] = Field(default_factory=list)

    def status(self, assets: Assets) -> GiftCodeCreationStatus:
        min_activations: int = assets.gift_codes.min_activations
        max_activations: int = assets.gift_codes.max_activations
        min_amount: float = assets.gift_codes.min_amount
        max_amount: float = assets.gift_codes.max_amount
        if self.activations is not None and not (
            min_activations <= self.activations <= max_activations
        ):
            return GiftCodeCreationStatus.ACTIVATIONS_LIMIT
        if self.amount is not None and not (min_amount <= self.amount <= max_amount):
            return GiftCodeCreationStatus.AMOUNT_LIMIT
        if self.amount is None or self.activations is None:
            return GiftCodeCreationStatus.NOT_READY
        return GiftCodeCreationStatus.READY

    def usd_amount(self, ton_rate: Optional[float] = None) -> Optional[float]:
        if ton_rate is None or self.amount is None:
            return None
        return round(self.amount * ton_rate, 2)


class FullGiftCodeData(PydanticModel):
    owner_address: str
    total_activations: int
    max_activations: int
    max_buy_amount: float

    @property
    def activations_left(self) -> int:
        return self.max_activations - self.total_activations


class GiftCodeActivation(PydanticModel):
    link_id: UUID
    contract_address: str
    seed: str
    message_id: int
