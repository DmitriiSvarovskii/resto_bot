__all__ = ("router",)

from aiogram import Router

from .customer_handlers import router as customer_routers
from .admin_handlers import router as admin_routers


router = Router(name=__name__)

router.include_routers(
    customer_routers,
    admin_routers
)
