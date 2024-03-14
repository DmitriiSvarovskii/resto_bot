from src.schemas import category_schemas


async def create_data_category(
    data: dict
):
    data_category = category_schemas.CreateCategory(
        name=data['name'],
        availability=data['availability'],
    )

    return data_category
