from __future__ import annotations

from typing import cast

from aiogram import Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.const import DEFAULT_LOCALE, MESSAGES_SOURCE_DIR
from app.models.config import AppConfig
from app.utils.localization import UserManager


def create_i18n_core(config: AppConfig) -> FluentRuntimeCore:
    locales: list[str] = cast(list[str], config.telegram.locales)
    return FluentRuntimeCore(
        path=MESSAGES_SOURCE_DIR / "{locale}",
        raise_key_error=False,
        locales_map={locales[i]: locales[i + 1] for i in range(len(locales) - 1)},
    )


def create_i18n_middleware(config: AppConfig) -> I18nMiddleware:
    return I18nMiddleware(
        core=create_i18n_core(config=config),
        manager=UserManager(),
        default_locale=DEFAULT_LOCALE,
    )


def setup_i18n_middleware(dispatcher: Dispatcher, config: AppConfig) -> None:
    middleware: I18nMiddleware = create_i18n_middleware(config=config)
    for event_type in dispatcher.resolve_used_update_types():
        dispatcher.observers[event_type].middleware(middleware)
    dispatcher.error.middleware(middleware)
    dispatcher.startup.register(middleware.core.startup)
    dispatcher.shutdown.register(middleware.core.shutdown)
    dispatcher.startup.register(middleware.manager.startup)
    dispatcher.shutdown.register(middleware.manager.shutdown)
    if middleware.enabled_startup:
        dispatcher.startup.register(middleware.startup)
    dispatcher[middleware.middleware_key] = middleware
