from typing import Final

from aiogram import Router

from . import confirm_creation, edit_creation, share, start_creation, use

router: Final[Router] = Router(name=__name__)
router.include_routers(
    confirm_creation.router,
    edit_creation.router,
    share.router,
    start_creation.router,
    use.router,
)
