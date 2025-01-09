from pydantic import Field

from ..types import Recipient
from .base import SplitMethod


class ResolveStarsRecipient(
    SplitMethod[Recipient],
    api_method="/recipients/stars",
    returning=Recipient,
    response_data_key=["message"],
):
    username: str = Field(description="Product recipient's username")
