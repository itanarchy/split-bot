from typing import Optional

from ..types import User
from .base import SplitMethod


class CreateUser(
    SplitMethod[User],
    api_method="/user/create",
    returning=User,
    response_data_key=["user"],
):
    inviter: Optional[str] = None
