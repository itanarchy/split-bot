from .base import SplitObject


class TransactionMessage(SplitObject):
    address: str
    amount: int
    payload: str
