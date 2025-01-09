from pydantic import Field

from ..types import Transaction
from .base import SplitMethod


class UseGiftCode(
    SplitMethod[Transaction],
    api_method="/gift-code/use",
    returning=Transaction,
    response_data_key=["message"],
):
    seed: str = Field(description="Gift code seed")
    amount: float = Field(description="Ton buy amount")
    recipient: str = Field(description="Telegram Stars recipient")
    gift_code_address: str = Field(description="Gift code contract address")
    owner_address: str = Field(description="Gift code owner address")
