from pydantic_settings import SettingsConfigDict

from app.utils.yaml import YAMLSettings, find_assets_sources

from .gift_codes import GiftCodesConfig
from .shop import ShopConfig
from .ton_connect import TonConnectConfig


class Assets(YAMLSettings):
    gift_codes: GiftCodesConfig
    shop: ShopConfig
    ton_connect: TonConnectConfig

    model_config = SettingsConfigDict(
        yaml_file_encoding="utf-8",
        yaml_file=find_assets_sources(),
    )
