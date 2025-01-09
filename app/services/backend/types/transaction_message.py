from typing import Optional

from pydantic import Field

from .base import SplitObject


class TransactionMessage(SplitObject):
    address: str = Field(description="Recipient address")
    amount: int = Field(description="Amount of TON to send")
    payload: Optional[str] = Field(
        description="Transaction payload",
        default=None,
    )
    state_init: Optional[str] = Field(
        default=None,
        description="Transaction state init",
        serialization_alias="stateInit",
    )
