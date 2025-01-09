from pydantic import Field

from .base import SplitObject
from .transaction import Transaction


class NewGiftCode(SplitObject):
    transaction: Transaction = Field(
        description="Transaction body. Must be sent via TON Connect or executed manually.",
    )
    seed: str = Field(description="Gift code seed")
    address: str = Field(description="Gift code address")
