from typing import Optional

from ..types import NewGiftCode
from .base import SplitMethod


class CreateGiftCode(
    SplitMethod[NewGiftCode],
    api_method="/gift-code/create",
    returning=NewGiftCode,
    response_data_key=["message"],
):
    seed: Optional[str] = None
    max_activations: int
    max_buy_amount: float
