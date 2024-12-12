from ..types import Transaction
from .base import SplitMethod


class BuyStars(
    SplitMethod[Transaction],
    api_method="/buy/stars",
    returning=Transaction,
    response_data_key=["transaction"],
):
    recipient: str
    quantity: int
