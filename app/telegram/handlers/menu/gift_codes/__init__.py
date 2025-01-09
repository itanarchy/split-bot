from typing import Final

from aiogram import Router

from . import confirm_creation, edit_creation, start_creation, use

router: Final[Router] = Router(name=__name__)
router.include_routers(
    confirm_creation.router,
    edit_creation.router,
    start_creation.router,
    use.router,
)
