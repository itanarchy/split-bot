from stollen.enums import HTTPMethod

from .base import SplitMethod


class GetBuyFee(
    SplitMethod[float],
    http_method=HTTPMethod.GET,
    api_method="/buy/fee",
    returning=float,
    response_data_key=["fee"],
):
    pass
