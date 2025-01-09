from pydantic import Field

from .base import MutableSplitObject
from .ton_proof_domain import TonProofDomain


class TonProof(MutableSplitObject):
    timestamp: int = Field(description="Proof timestamp")
    domain: TonProofDomain = Field(description="Proof domain")
    signature: str = Field(description="Proof signature")
    payload: str = Field(description="Custom proof payload")
    state_init: str = Field(description="State init")
