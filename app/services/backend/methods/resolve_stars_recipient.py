from ..types import Recipient
from .base import SplitMethod


class ResolveStarsRecipient(
    SplitMethod[Recipient],
    api_method="/recipients/stars",
    returning=Recipient,
):
    username: str
