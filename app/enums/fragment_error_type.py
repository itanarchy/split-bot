from enum import StrEnum, auto


class FragmentErrorType(StrEnum):
    ALREADY_PREMIUM = auto()
    USERNAME_NOT_ASSIGNED = auto()
    USERNAME_NOT_FOUND = auto()
    UNKNOWN = auto()
