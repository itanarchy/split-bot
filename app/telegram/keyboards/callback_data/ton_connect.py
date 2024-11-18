from aiogram.filters.callback_data import CallbackData


class CDLinkWallet(CallbackData, prefix="link_wallet"):
    pass


class CDUnlinkWallet(CallbackData, prefix="unlink_wallet"):
    pass


class CDChooseWallet(CallbackData, prefix="choose_wallet"):
    wallet_name: str


class CDCancelConnection(CallbackData, prefix="cancel_connection"):
    task_id: str
