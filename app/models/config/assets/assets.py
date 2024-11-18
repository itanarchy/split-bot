from pydantic_settings import SettingsConfigDict

from app.utils.yaml import YAMLSettings, find_assets_sources

from .shop import ShopConfig
from .ton_connect import TonConnect


class Assets(YAMLSettings):
    shop: ShopConfig
    ton_connect: TonConnect

    model_config = SettingsConfigDict(
        yaml_file_encoding="utf-8",
        yaml_file=find_assets_sources(),
    )
