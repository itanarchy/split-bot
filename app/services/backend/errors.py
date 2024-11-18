from stollen.exceptions import StollenAPIError


class SplitAPIError(StollenAPIError):
    pass


class SplitBadRequestError(SplitAPIError):
    pass


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
