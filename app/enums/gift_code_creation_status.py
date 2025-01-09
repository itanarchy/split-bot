from enum import StrEnum, auto


class GiftCodeCreationStatus(StrEnum):
    NOT_READY = auto()
    ACTIVATIONS_LIMIT = auto()
    AMOUNT_LIMIT = auto()
    READY = auto()
