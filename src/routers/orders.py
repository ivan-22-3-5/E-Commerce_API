from fastapi import APIRouter, status

from src.crud import orders, products
from src.schemas.order import OrderIn, OrderOut
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceDoesNotExistError

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order(order: OrderIn, user: cur_user_dependency, db: db_dependency):
    if not await products.get_by_id(order.product_id, db):
        raise ResourceDoesNotExistError("Product with the given id does not exist")
    return await orders.create(order, user.id, db=db)

