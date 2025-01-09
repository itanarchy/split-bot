from app.models.base import PydanticModel


class TonConnectConfig(PydanticModel):
    manifest_url: str
    timeout: int
