from typing import Final

from aiogram.filters import Filter, StateFilter
from aiogram.fsm.state import State, StatesGroup

NoneState: Final[Filter] = StateFilter(None)
AnyState: Final[Filter] = ~NoneState


class SGBuyPremium(StatesGroup):
    enter_username = State()
    select_period = State()
    # select_currency = State()
    confirm = State()


class SGBuyStars(StatesGroup):
    enter_username = State()
    enter_count = State()
    # select_currency = State()
    confirm = State()


class SGCreateGiftCode(StatesGroup):
    waiting = State()
    amount = State()
    activations = State()


class SGUseGiftCode(StatesGroup):
    username = State()
