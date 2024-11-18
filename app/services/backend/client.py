from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from stollen import Stollen

from .errors import (
    SplitAPIError,
    SplitBadRequestError,
    SplitConflictError,
    SplitInternalError,
    SplitMethodNotAllowedError,
    SplitNotFoundError,
    SplitUnauthorizedError,
)

if TYPE_CHECKING:
    from .types import (
        Recipient,
        TonProof,
        Transaction,
        User,
    )


class Backend(Stollen):
    def __init__(self, *, base_url: str, **stollen_kwargs: Any) -> None:
        super().__init__(
            base_url=base_url,
            response_data_key=["message"],
            error_message_key=["error_message"],
            general_error_class=SplitAPIError,
            error_codes={
                400: SplitBadRequestError,
                401: SplitUnauthorizedError,
                404: SplitNotFoundError,
                405: SplitMethodNotAllowedError,
                409: SplitConflictError,
                500: SplitInternalError,
            },
            **stollen_kwargs,
        )

    async def buy_premium(
        self,
        access_token: str,
        recipient: str,
        months: int,
    ) -> Transaction:
        from .methods import BuyPremium

        call: BuyPremium = BuyPremium(
            access_token=access_token,
            recipient=recipient,
            months=months,
        )

        return await self(call)

    async def buy_stars(
        self,
        access_token: str,
        recipient: str,
        quantity: int,
    ) -> Transaction:
        from .methods import BuyStars

        call: BuyStars = BuyStars(
            access_token=access_token,
            recipient=recipient,
            quantity=quantity,
        )

        return await self(call)

    async def check_ton_proof(
        self,
        address: str,
        network: str,
        public_key: str,
        proof: TonProof,
    ) -> str:
        from .methods import CheckTonProof

        call: CheckTonProof = CheckTonProof(
            address=address,
            network=network,
            public_key=public_key,
            proof=proof,
        )

        return await self(call)

    async def create_user(self, access_token: str, inviter: Optional[str] = None) -> User:
        from .methods import CreateUser

        call: CreateUser = CreateUser(access_token=access_token, inviter=inviter)

        return await self(call)

    async def generate_ton_proof_payload(self) -> str:
        from .methods import GenerateTonProofPayload

        call: GenerateTonProofPayload = GenerateTonProofPayload()

        return await self(call)

    async def get_me(self, access_token: str) -> User:
        from .methods import GetMe

        call: GetMe = GetMe(access_token=access_token)

        return await self(call)

    async def resolve_premium_recipient(self, access_token: str, username: str) -> Recipient:
        from .methods import ResolvePremiumRecipient

        call: ResolvePremiumRecipient = ResolvePremiumRecipient(
            access_token=access_token,
            username=username,
        )

        return await self(call)

    async def resolve_stars_recipient(self, access_token: str, username: str) -> Recipient:
        from .methods import ResolveStarsRecipient

        call: ResolveStarsRecipient = ResolveStarsRecipient(
            access_token=access_token,
            username=username,
        )

        return await self(call)
