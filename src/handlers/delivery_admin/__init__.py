__all__ = ("router",)

from aiogram import Router
from .change_delivery_base import router as change_delivery_router
from .fsm_add_district import router as add_district_router


router = Router(name=__name__)

router.include_routers(
    change_delivery_router,
    add_district_router,
)
