from .base import BotError


class TonConnectError(BotError):
    pass


class InvalidTonProofError(TonConnectError):
    pass


class TonIsAlreadyConnectedError(TonConnectError):
    pass
