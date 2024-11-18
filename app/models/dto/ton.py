from uuid import uuid4

from pydantic import Field

from app.models.base import PydanticModel


class TonWallet(PydanticModel):
    name: str
    image: str
    about_url: str
    app_name: str
    bridge_url: str
    universal_url: str


class TonConnection(PydanticModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    url: str
    ton_proof: str


class TonConnectResult(PydanticModel):
    address: str
    access_token: str
