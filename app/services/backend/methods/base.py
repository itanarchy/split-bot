from stollen import StollenMethod
from stollen.enums import HTTPMethod
from stollen.types import StollenT

from ..client import Backend


class SplitMethod(
    StollenMethod[StollenT, Backend],
    http_method=HTTPMethod.POST,
    abstract=True,
):
    pass
