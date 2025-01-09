from __future__ import annotations

from typing import Protocol, TypeAlias, Union, cast

from pytoniq_core import Address


class HasAddress(Protocol):
    address: Address | str


AddressType: TypeAlias = Union[HasAddress, Address, str]


def convert_address(
    source: AddressType,
    is_user_friendly: bool = True,
    is_url_safe: bool = True,
    is_bounceable: bool = False,
    is_test_only: bool = False,
) -> str:
    if hasattr(source, "address"):
        source = source.address
    return cast(
        str,
        Address(source).to_str(
            is_user_friendly=is_user_friendly,
            is_url_safe=is_url_safe,
            is_bounceable=is_bounceable,
            is_test_only=is_test_only,
        ),
    )


def short_address(address: AddressType) -> str:
    address = convert_address(address)
    return f"{address[:6]}...{address[-6:]}"
