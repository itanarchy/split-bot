from app.models.base import PydanticModel


class GiftCodesConfig(PydanticModel):
    min_activations: int
    max_activations: int
    min_amount: float
    max_amount: float
