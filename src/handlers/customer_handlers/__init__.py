__all__ = ("router",)

from aiogram import Router

from .cart_handlers import router as cart_router
from .fsm_comment import router as fsm_comment_router
from .fsm_delivery import router as fsm_delivery_router
from .main_menu_handlers import router as main_menu_router
from .menu_handlers import router as menu_router
from .order_handlers import router as order_router
from .select_store import router as select_store_router
from .start_handlers import router as start_router
from .common_handlers import router as common_router

router = Router(name=__name__)

router.include_routers(
    common_router,
    start_router,
    select_store_router,
    main_menu_router,
    menu_router,
    fsm_comment_router,
    fsm_delivery_router,
    cart_router,
    order_router,
)
