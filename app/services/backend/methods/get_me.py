from stollen.enums import HTTPMethod

from ..types import User
from .base import SplitMethod


class GetMe(
    SplitMethod[User],
    http_method=HTTPMethod.GET,
    api_method="/user/get",
    returning=User,
    response_data_key=["user"],
):
    pass
