from datetime import datetime
from typing import Optional

from .base import SplitObject


class User(SplitObject):
    id: int
    created_at: datetime
    wallet_address: str
    inviter: Optional[str] = None
