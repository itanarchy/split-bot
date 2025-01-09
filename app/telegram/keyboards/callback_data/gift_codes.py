from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class CDSetGiftCodeAmount(CallbackData, prefix="gift_code_amount"):
    pass


class CDSetGiftCodeActivations(CallbackData, prefix="gift_code_activations"):
    pass


class CDConfirmGiftCode(CallbackData, prefix="confirm_gift_code"):
    pass


class CDCreateGiftCode(CallbackData, prefix="create_gift_code"):
    pass


class CDUseGiftCode(CallbackData, prefix="use_gc"):
    link_id: UUID
