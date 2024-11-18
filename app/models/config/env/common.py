from .base import EnvSettings


class CommonConfig(EnvSettings, env_prefix="COMMON_"):
    admin_chat_id: int = 5945468457
    backend_url: str = "https://api.split.tg/"
    users_cache_time: int = 15
    ton_connect_cache_time: int = 15
