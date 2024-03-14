from src.schemas import product_schemas


async def create_data_product(
    data: dict
):
    data_product = product_schemas.CreateProduct(
        category_id=data['category_id'],
        name=data['name'],
        description=data['description'],
        price=data['price'],
        price_box=data['price_box'],
        availability=data['availability'],
    )

    return data_product
