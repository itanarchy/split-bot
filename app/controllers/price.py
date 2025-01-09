from app.models.base import PydanticModel
from app.models.config import Assets
from app.services.backend import Backend


class PriceDto(PydanticModel):
    usd_price: float
    ton_price: float


async def get_price(base_usd_price: float, backend: Backend) -> PriceDto:
    fee: float = await backend.get_buy_fee()
    ton_price_usd: float = await backend.get_ton_rate()
    usd_price: float = base_usd_price * (1 + fee)
    return PriceDto(
        usd_price=usd_price,
        ton_price=usd_price / ton_price_usd,
    )


async def get_stars_price(quantity: int, backend: Backend, assets: Assets) -> PriceDto:
    return await get_price(base_usd_price=quantity * assets.shop.stars_price, backend=backend)


async def get_premium_price(months: int, backend: Backend, assets: Assets) -> PriceDto:
    return await get_price(
        base_usd_price=assets.shop.subscription_periods[months],
        backend=backend,
    )
