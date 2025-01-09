from typing import Final

from aiogram import Router

from . import premium, stars

router: Final[Router] = Router(name=__name__)
router.include_routers(premium.router, stars.router)
