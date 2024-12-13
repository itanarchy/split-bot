from aiogram.contrib.paginator import CDPagination as _CDPagination
from aiogram.filters.callback_data import CallbackData


class CDMenu(CallbackData, prefix="menu"):
    pass


class CDTelegramPremium(CallbackData, prefix="telegram_premium"):
    pass


class CDTelegramStars(CallbackData, prefix="telegram_stars"):
    pass


class CDLanguage(CallbackData, prefix="language"):
    pass


class CDSetLanguage(CallbackData, prefix="set_language"):
    locale: str


class CDReferralProgram(CallbackData, prefix="referral_program"):
    pass


class CDPagination(_CDPagination, prefix="pt"):
    pass
