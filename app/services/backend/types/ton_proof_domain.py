from pydantic import Field

from .base import MutableSplitObject


class TonProofDomain(MutableSplitObject):
    length_bytes: int = Field(alias="lengthBytes")
    value: str
