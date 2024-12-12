from ..types import Transaction
from .base import SplitMethod


class BuyPremium(
    SplitMethod[Transaction],
    api_method="/buy/premium",
    returning=Transaction,
    response_data_key=["transaction"],
):
    recipient: str
    months: int
