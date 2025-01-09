from stollen.enums import HTTPMethod

from .base import SplitMethod


class GetTonRate(
    SplitMethod[float],
    http_method=HTTPMethod.GET,
    api_method="/buy/ton_rate",
    returning=float,
    response_data_key=["ton_rate"],
):
    pass
