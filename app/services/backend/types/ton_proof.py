from .base import MutableSplitObject
from .ton_proof_domain import TonProofDomain


class TonProof(MutableSplitObject):
    timestamp: int
    domain: TonProofDomain
    signature: str
    payload: str
    state_init: str
