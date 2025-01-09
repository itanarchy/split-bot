from __future__ import annotations

from typing import Final, Optional, cast

DEFAULT_TON_DECIMALS: Final[int] = 9


def from_nano(
    value: int,
    decimals: int = DEFAULT_TON_DECIMALS,
    precision: Optional[int] = None,
) -> float:
    if not isinstance(value, int) or value < 0:
        raise ValueError("Value must be a positive integer.")
    if precision is not None and precision < 0:
        raise ValueError("Precision must be a non-negative integer.")
    ton_value: float = value / (10**decimals)
    if precision is None:
        return ton_value
    return round(ton_value, precision)


def to_nano(value: float, decimals: int = DEFAULT_TON_DECIMALS) -> int:
    return cast(int, round(value * (10**decimals)))
