from ..types import Transaction
from .base import SplitMethod


class BuyStars(
    SplitMethod[Transaction],
    api_method="/buy/stars",
    returning=Transaction,
):
    recipient: str
    quantity: int
