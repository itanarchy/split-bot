from ..types import Recipient
from .base import SplitMethod


class ResolvePremiumRecipient(
    SplitMethod[Recipient],
    api_method="/recipients/premium",
    returning=Recipient,
):
    username: str
