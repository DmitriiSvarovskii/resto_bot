from .cart import CartEditCallbackFactory


class ProductIdCallbackFactory(
    CartEditCallbackFactory,
    prefix='pr',
):
    category_id: int


class ProductIdAdminCallbackFactory(
    ProductIdCallbackFactory,
    prefix='prad',
):
    pass
