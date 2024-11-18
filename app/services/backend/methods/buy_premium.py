from ..types import Transaction
from .base import SplitMethod


class BuyPremium(
    SplitMethod[Transaction],
    api_method="/buy/premium",
    returning=Transaction,
):
    recipient: str
    months: int
