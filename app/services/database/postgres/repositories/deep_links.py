from typing import Any, Optional
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument

from app.enums import DeepLinkAction
from app.models.sql import DeepLink

from .base import BaseRepository


class DeepLinksRepository(BaseRepository):
    async def get(self, link_id: UUID) -> Optional[DeepLink]:
        return await self._get(DeepLink, DeepLink.id == link_id)

    async def by_owner(
        self,
        owner_id: int,
        action: Optional[DeepLinkAction] = None,
    ) -> Optional[DeepLink]:
        conditions: list[ColumnExpressionArgument[Any]] = [DeepLink.owner_id == owner_id]
        if action is not None:
            conditions.append(DeepLink.action == action)
        return await self._get(DeepLink, DeepLink.owner_id == owner_id)
