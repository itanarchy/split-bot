from typing import Optional

from pydantic import Field

from .base import SplitObject
from .transaction_message import TransactionMessage


class Transaction(SplitObject):
    valid_until: Optional[int] = Field(
        default=None,
        validation_alias="validUntil",
        serialization_alias="valid_until",
    )
    from_address: Optional[str] = Field(default=None, alias="from")
    network: Optional[int] = Field(default=None, alias="network")
    messages: list[TransactionMessage]
