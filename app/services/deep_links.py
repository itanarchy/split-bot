from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.enums import DeepLinkAction
from app.models.config import AppConfig
from app.models.dto import DeepLinkDto
from app.models.sql import DeepLink
from app.services.database import RedisRepository, SQLSessionContext


class DeepLinksService:
    session_pool: async_sessionmaker[AsyncSession]
    redis: RedisRepository
    config: AppConfig

    def __init__(
        self,
        session_pool: async_sessionmaker[AsyncSession],
        redis: RedisRepository,
        config: AppConfig,
    ) -> None:
        self.session_pool = session_pool
        self.redis = redis
        self.config = config

    async def create(
        self,
        owner_id: int,
        action: DeepLinkAction = DeepLinkAction.INVITE,
        gift_code_address: Optional[str] = None,
        gift_code_seed: Optional[str] = None,
    ) -> DeepLinkDto:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            deep_link: DeepLink = DeepLink(
                owner_id=owner_id,
                action=action,
                gift_code_address=gift_code_address,
                gift_code_seed=gift_code_seed,
            )
            await uow.commit(deep_link)
        return deep_link.dto()

    async def get(self, link_id: UUID) -> Optional[DeepLinkDto]:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            deep_link_dto: Optional[DeepLinkDto] = await self.redis.get_deep_link(link_id=link_id)
            if deep_link_dto is None:
                deep_link: Optional[DeepLink] = await repository.deep_links.get(link_id=link_id)
                if deep_link is None:
                    return None
                deep_link_dto = deep_link.dto()
                await self.redis.save_deep_link(
                    link=deep_link_dto,
                    cache_time=self.config.common.deep_links_cache_time,
                )
            return deep_link_dto

    async def get_invite_link(self, owner_id: int) -> DeepLinkDto:
        async with SQLSessionContext(self.session_pool) as (repository, uow):
            deep_link: Optional[DeepLink] = await repository.deep_links.by_owner(
                owner_id=owner_id,
                action=DeepLinkAction.INVITE,
            )
            if deep_link is None:
                return await self.create(owner_id=owner_id)
            return deep_link.dto()
