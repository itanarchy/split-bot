from typing import Final

from aiogram import Router

from . import gift_codes, language, main, referral_program, shop

router: Final[Router] = Router(name=__name__)
router.include_routers(
    gift_codes.router,
    main.router,
    shop.router,
    language.router,
    referral_program.router,
)
