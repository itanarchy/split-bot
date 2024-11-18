from __future__ import annotations

import base64
import logging
from typing import TYPE_CHECKING, Final

from pytonconnect import TonConnect
from pytonconnect.parsers import TonProof as _TonProof
from stollen.exceptions import StollenAPIError

from app.exceptions.ton_connect import InvalidTonProofError
from app.services.backend.types import TonProof, TonProofDomain
from app.utils.ton import convert_address

if TYPE_CHECKING:
    from app.services.backend import Backend

logger: Final[logging.Logger] = logging.getLogger(__name__)


async def verify_ton_proof(connector: TonConnect, backend: Backend) -> str:
    proof: _TonProof = connector.wallet.ton_proof
    try:
        return await backend.check_ton_proof(
            address=convert_address(connector.account, is_user_friendly=False),
            network=connector.account.chain,
            public_key=connector.account.public_key,
            proof=TonProof(
                timestamp=proof.timestamp,
                domain=TonProofDomain(length_bytes=proof.domain_len, value=proof.domain_val),
                signature=base64.b64encode(proof.signature).decode(),
                payload=proof.payload,
                state_init=connector.account.wallet_state_init,
            ),
        )
    except StollenAPIError as error:
        logger.error(error, exc_info=True)
        raise InvalidTonProofError()
