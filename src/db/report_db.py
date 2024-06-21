from typing import Optional, List

from src.crud import report_crud, product_crud
from src.db.database import get_async_session
from src.schemas import delivery_schemas, customer_schemas


async def get_sales_period_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    async for session in get_async_session():
        response = await report_crud.crud_get_sales_period_summary(
            start_date=start_date,
            end_date=end_date,
            session=session
        )
        return response


async def get_stop_list(
    store_id: int
):
    async for session in get_async_session():
        response = await product_crud.crud_get_stop_list(
            store_id=store_id,
            session=session
        )
        return response


async def get_delivery_report() -> List[
    delivery_schemas.ReadDeliveryReport
]:
    async for session in get_async_session():
        response = await report_crud.crud_get_delivery_report(
            session=session
        )
        return response


async def get_resourse_report(resourse: str) -> Optional[
    customer_schemas.CustomerAdResourse
]:
    async for session in get_async_session():
        response = await report_crud.crud_get_resourse_report(
            resourse=resourse,
            session=session
        )
        return response
