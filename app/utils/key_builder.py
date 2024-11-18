from decimal import Decimal
from enum import Enum
from fractions import Fraction
from typing import TYPE_CHECKING, Any, ClassVar, Optional
from uuid import UUID

from pydantic import BaseModel


class StorageKey(BaseModel):
    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        """Data separator (default is :code:`:`)"""
        __prefix__: ClassVar[Optional[str]]
        """Callback prefix"""

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, **kwargs: Any) -> None:
        cls.__separator__ = kwargs.pop("separator", ":")
        cls.__prefix__ = kwargs.pop("prefix", None)
        if cls.__separator__ in (cls.__prefix__ or ""):
            raise ValueError(
                f"Separator symbol {cls.__separator__!r} can not be used "
                f"inside prefix {cls.__prefix__!r}"
            )
        super().__init_subclass__(**kwargs)

    @classmethod
    def encode_value(cls, key: str, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        if isinstance(value, (int, str, float, Decimal, Fraction)):
            return str(value)
        raise ValueError(
            f"Attribute {key}={value!r} of type {type(value).__name__!r}"
            f" can not be packed to callback data"
        )

    def pack(self) -> str:
        result = [self.__prefix__] if self.__prefix__ else []
        for key, value in self.model_dump(mode="json").items():
            encoded = self.encode_value(key, value)
            if self.__separator__ in encoded:
                raise ValueError(
                    f"Separator symbol {self.__separator__!r} can not be used "
                    f"in value {key}={encoded!r}"
                )
            result.append(encoded)
        return self.__separator__.join(result)
