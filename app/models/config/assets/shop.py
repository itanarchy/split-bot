from app.models.base import PydanticModel


class ShopConfig(PydanticModel):
    available_tickers: list[str]
    min_stars: int
    max_stars: int
    subscription_periods: dict[int, int]
    stars_price: float
