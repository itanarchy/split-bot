from ..types import TonProof
from .base import PublicSplitMethod


class CheckTonProof(
    PublicSplitMethod[str],
    api_method="/ton-proof/check_proof",
    returning=str,
    response_data_key=["token"],
):
    address: str
    network: str
    public_key: str
    proof: TonProof
