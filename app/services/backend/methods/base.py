from pydantic import field_validator
from stollen import StollenMethod
from stollen.enums import HTTPMethod
from stollen.requests import HeaderField
from stollen.types import StollenT

from ..client import Backend


class SplitMethod(
    StollenMethod[StollenT, Backend],
    http_method=HTTPMethod.POST,
    abstract=True,
):
    access_token: str = HeaderField(serialization_alias="Authorization")

    @field_validator("access_token", mode="before")
    def wrap_access_token(cls, value: str) -> str:
        return f"Bearer {value}"


class PublicSplitMethod(
    StollenMethod[StollenT, Backend],
    http_method=HTTPMethod.POST,
    abstract=True,
):
    pass
