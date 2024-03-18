from src.schemas import delivery_schemas


async def create_data_district(
    data: dict
):
    data_district = delivery_schemas.CreateDelivery(**data)

    return data_district
