from typing import Final

from aiogram import Router

from . import link, select, unlink

router: Final[Router] = Router(name=__name__)
router.include_routers(
    link.router,
    select.router,
    unlink.router,
)
