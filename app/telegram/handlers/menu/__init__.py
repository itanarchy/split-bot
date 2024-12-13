from typing import Final

from aiogram import Router

from . import buy_premium, buy_stars, language, main, referral_program

router: Final[Router] = Router(name=__name__)
router.include_routers(
    main.router,
    buy_premium.router,
    buy_stars.router,
    language.router,
    referral_program.router,
)
