from typing import Any

from stollen.exceptions import StollenAPIError

from app.enums import FragmentErrorType


def detect_fragment_error_type(message: str) -> str:
    if message == "This account is already subscribed to Telegram Premium.":
        return FragmentErrorType.ALREADY_PREMIUM
    if message == "Please enter a username assigned to a user.":
        return FragmentErrorType.USERNAME_NOT_ASSIGNED
    if message == "No Telegram users found.":
        return FragmentErrorType.USERNAME_NOT_FOUND
    return message


class SplitAPIError(StollenAPIError):
    pass


class SplitBadRequestError(SplitAPIError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message=detect_fragment_error_type(message), **kwargs)


class SplitUnauthorizedError(SplitAPIError):
    pass


class SplitNotFoundError(SplitAPIError):
    pass


class SplitMethodNotAllowedError(SplitAPIError):
    pass


class SplitConflictError(SplitAPIError):
    pass


class SplitInternalError(SplitAPIError):
    pass
