from pydantic import SecretStr

from .base import EnvSettings


class CommonConfig(EnvSettings, env_prefix="COMMON_"):
    admin_chat_id: int = 5945468457
    backend_url: str = "https://api.split.tg/"
    users_cache_time: int = 30
    deep_links_cache_time: int = 300
    ton_connect_cache_time: int = 30
    ton_center_key: SecretStr = SecretStr("")
    ton_api_bridge_key: SecretStr = SecretStr("")
