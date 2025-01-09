from typing import Optional

from pydantic import Field

from ..types import User
from .base import SplitMethod


class CreateUser(
    SplitMethod[User],
    api_method="/user/create",
    returning=User,
    response_data_key=["message", "user"],
):
    inviter: Optional[str] = Field(default=None, description="Inviter's wallet address")
