from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import SplitObject


class User(SplitObject):
    id: int = Field(description="Internal user ID")
    created_at: datetime = Field(description="User's registration timestamp")
    wallet_address: str = Field(description="User's wallet address")
    inviter: Optional[str] = Field(default=None, description="Inviter's wallet address")
