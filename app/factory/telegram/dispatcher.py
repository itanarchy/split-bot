from __future__ import annotations

from aiogram import Dispatcher, F
from aiogram.contrib.paginator import PaginationFactory
from aiogram.enums import ChatType
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from redis.asyncio import Redis
from stollen.requests import RequestSerializer

from app.enums import MiddlewareEventType
from app.factory.redis import create_redis
from app.factory.session_pool import create_session_pool
from app.factory.telegram.i18n import setup_i18n_middleware
from app.models.config import AppConfig, Assets
from app.services.backend import Backend
from app.services.backend.session import BackendSession
from app.services.database import RedisRepository
from app.services.task_manager import TaskManager
from app.telegram.handlers import admin, extra, menu, ton_connect
from app.telegram.helpers.paginator import Paginator
from app.telegram.keyboards.callback_data.menu import CDPagination
from app.telegram.middlewares import (
    MessageHelperMiddleware,
    TonConnectMiddleware,
    UserMiddleware,
)
from app.utils import mjson


def setup_pagination(dispatcher: Dispatcher) -> None:
    PaginationFactory(
        paginator_cls=Paginator,
        page_button_data=CDPagination,
        rows_per_page=5,
    ).register(
        dispatcher,
        MiddlewareEventType.MESSAGE,
        MiddlewareEventType.CALLBACK_QUERY,
    )


def create_dispatcher(config: AppConfig) -> Dispatcher:
    redis: Redis = create_redis(url=config.redis.build_url())

    # noinspection PyArgumentList
    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        config=config,
        session_pool=create_session_pool(config=config),
        redis=RedisRepository(client=redis),
        task_manager=TaskManager(),
        assets=Assets(),
        backend=Backend(
            base_url=config.common.backend_url,
            session=BackendSession(serializer=RequestSerializer(exclude_defaults=False)),
        ),
    )

    dispatcher.include_routers(
        admin.router,
        menu.router,
        ton_connect.router,
        extra.router,
    )
    dispatcher.message.filter(F.chat.type == ChatType.PRIVATE)
    dispatcher.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)

    UserMiddleware().setup_inner(router=dispatcher)
    setup_i18n_middleware(dispatcher=dispatcher, config=config)
    MessageHelperMiddleware().setup_inner(router=dispatcher)
    setup_pagination(dispatcher)
    TonConnectMiddleware().setup_inner(router=dispatcher)
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
