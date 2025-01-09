from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

from stollen import Stollen
from stollen.requests import Header

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
        NewGiftCode,
        Recipient,
        TonProof,
        Transaction,
        User,
    )


class Backend(Stollen):
    access_token: Optional[str] = None

    def __init__(
        self,
        *,
        base_url: str,
        access_token: Optional[str] = None,
        **stollen_kwargs: Any,
    ) -> None:
        self.access_token = access_token
        super().__init__(
            base_url=base_url,
            error_message_key=["error_message"],
            global_request_fields=[self.get_access_token_header],
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

    def get_access_token_header(self, *_: Any) -> Header:
        return Header(name="Authorization", value=f"Bearer {self.access_token}")

    async def buy_premium(self, recipient: str, months: int) -> Transaction:
        from .methods import BuyPremium

        call: BuyPremium = BuyPremium(
            recipient=recipient,
            months=months,
        )

        return await self(call)

    async def buy_stars(
        self,
        recipient: str,
        quantity: int,
    ) -> Transaction:
        from .methods import BuyStars

        call: BuyStars = BuyStars(recipient=recipient, quantity=quantity)

        return await self(call)

    async def check_ton_proof(
        self,
        address: str,
        network: Literal["-3", "-239"],
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

    async def create_gift_code(
        self,
        *,
        seed: Optional[str] = None,
        max_activations: int,
        max_buy_amount: float,
    ) -> NewGiftCode:
        from .methods import CreateGiftCode

        call: CreateGiftCode = CreateGiftCode(
            seed=seed,
            max_activations=max_activations,
            max_buy_amount=max_buy_amount,
        )

        return await self(call)

    async def create_user(self, inviter: Optional[str] = None) -> User:
        from .methods import CreateUser

        call: CreateUser = CreateUser(inviter=inviter)

        return await self(call)

    async def generate_ton_proof_payload(self) -> str:
        from .methods import GenerateTonProofPayload

        call: GenerateTonProofPayload = GenerateTonProofPayload()

        return await self(call)

    async def get_buy_fee(self) -> float:
        from .methods import GetBuyFee

        call: GetBuyFee = GetBuyFee()

        return await self(call)

    async def get_me(self) -> User:
        from .methods import GetMe

        call: GetMe = GetMe()

        return await self(call)

    async def get_ton_rate(self) -> float:
        from .methods import GetTonRate

        call: GetTonRate = GetTonRate()

        return await self(call)

    async def resolve_premium_recipient(self, username: str) -> Recipient:
        from .methods import ResolvePremiumRecipient

        call: ResolvePremiumRecipient = ResolvePremiumRecipient(username=username)

        return await self(call)

    async def resolve_stars_recipient(self, username: str) -> Recipient:
        from .methods import ResolveStarsRecipient

        call: ResolveStarsRecipient = ResolveStarsRecipient(username=username)

        return await self(call)

    async def use_gift_code(
        self,
        seed: str,
        amount: float,
        recipient: str,
        gift_code_address: str,
        owner_address: str,
    ) -> Transaction:
        from .methods import UseGiftCode

        call: UseGiftCode = UseGiftCode(
            seed=seed,
            amount=amount,
            recipient=recipient,
            gift_code_address=gift_code_address,
            owner_address=owner_address,
        )

        return await self(call)
