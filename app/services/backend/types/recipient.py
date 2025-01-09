from pydantic import Field

from .base import SplitObject


class Recipient(SplitObject):
    recipient: str = Field(description="Recipient address for Fragment invoice payment")
    photo: str = Field(description="Recipient's photo data as HTML image object")
    name: str = Field(description="Recipient's display name")
