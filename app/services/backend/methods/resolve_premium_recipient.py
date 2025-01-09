from pydantic import Field

from ..types import Recipient
from .base import SplitMethod


class ResolvePremiumRecipient(
    SplitMethod[Recipient],
    api_method="/recipients/premium",
    returning=Recipient,
    response_data_key=["message"],
):
    username: str = Field(description="Product recipient's username")
