from aiogram.filters.callback_data import CallbackData


class CDSelectSubscriptionPeriod(CallbackData, prefix="subscription_period"):
    period: int


class CDSelectCurrency(CallbackData, prefix="currency"):
    currency: str


class CDConfirmPurchase(CallbackData, prefix="confirm_purchase"):
    pass
