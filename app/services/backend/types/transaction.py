from pydantic import Field

from .base import SplitObject
from .transaction_message import TransactionMessage


class Transaction(SplitObject):
    messages: list[TransactionMessage] = Field(description="List of transaction messages")
    valid_until: int = Field(
        description="Transaction valid until timestamp",
        validation_alias="validUntil",
        serialization_alias="valid_until",
    )
