from pydantic import Field

from .base import MutableSplitObject


class TonProofDomain(MutableSplitObject):
    length_bytes: int = Field(alias="lengthBytes", description="Domain length")
    value: str = Field(description="Domain value")
