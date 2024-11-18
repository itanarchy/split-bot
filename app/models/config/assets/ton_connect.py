from app.models.base import PydanticModel


class TonConnect(PydanticModel):
    manifest_url: str
    timeout: int
