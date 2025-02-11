from pydantic import Field

from app.enums.payment_method import PaymentMethod

from ..types import Transaction
from .base import SplitMethod


class BuyPremium(
    SplitMethod[Transaction],
    api_method="/buy/premium",
    returning=Transaction,
    response_data_key=["message", "transaction"],
):
    recipient: str = Field(
        description=(
            "Recipient address for Fragment invoice payment. "
            "Can be found via search recipient method"
        ),
    )
    payment_method: PaymentMethod = Field(
        default=PaymentMethod.TON_CONNECT,
        description=(
            "Payment method. Default is transaction that "
            "must be sent via TON Connect or executed manually on TON chain"
        ),
    )
    months: int = Field(description="Subscription duration in months")
    username: str = Field(description="Recipient's username")
