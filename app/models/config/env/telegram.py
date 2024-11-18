from pydantic import SecretStr

from app.utils.custom_types import StringList

from .base import EnvSettings


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    locales: StringList
    drop_pending_updates: bool = False
    use_webhook: bool = False
    reset_webhook: bool = True
    webhook_path: str
    webhook_secret: SecretStr
