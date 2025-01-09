from typing import Literal

from pydantic import Field

from ..types import TonProof
from .base import SplitMethod


class CheckTonProof(
    SplitMethod[str],
    api_method="/ton-proof/check_proof",
    returning=str,
    response_data_key=["message", "token"],
):
    address: str = Field(description="Wallet address")
    network: Literal["-3", "-239"] = Field(
        description=(
            "Wallet masterchain ID represented represented as a string.\n"
            "-239 for the main network, -3 for the test network."
        )
    )
    public_key: str = Field(description="Wallet public key")
    proof: TonProof = Field(description="Wallet proof data")
