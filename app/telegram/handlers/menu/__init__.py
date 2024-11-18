from typing import Final

from aiogram import Router

from . import buy_premium, buy_stars, main

router: Final[Router] = Router(name=__name__)
router.include_routers(
    main.router,
    buy_premium.router,
    buy_stars.router,
)
