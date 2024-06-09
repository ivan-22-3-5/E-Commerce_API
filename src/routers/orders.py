from fastapi import APIRouter, status

from src.constraints import admin_path
from src.crud import orders, products
from src.custom_types import OrderStatus
from src.schemas.message import Message
from src.schemas.order import OrderIn, OrderOut
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceDoesNotExistError, NotEnoughRightsError

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderOut)
async def create_order(order: OrderIn, user: cur_user_dependency, db: db_dependency):
    if not await products.get_by_id(order.product_id, db):
        raise ResourceDoesNotExistError("Product with the given id does not exist")
    return await orders.create(order, user.id, db=db)


@router.patch('/{order_id}/cancel', status_code=status.HTTP_200_OK, response_model=Message)
async def cancel_order(order_id: int, user: cur_user_dependency, db: db_dependency):
    if (order := await orders.get_by_id(order_id, db)) is None:
        raise ResourceDoesNotExistError("Order with the given id does not exist")
    if order.user_id != user.id:
        raise NotEnoughRightsError("User is not order owner")
    await orders.update_status(order_id, OrderStatus.CANCELLED, db=db)
    return Message(message="The order cancelled")


@router.patch('/{order_id}/status', status_code=status.HTTP_200_OK, response_model=Message)
@admin_path
async def change_order_status(order_id: int, new_status: OrderStatus, db: db_dependency, user: cur_user_dependency):
    if not await orders.get_by_id(order_id, db):
        raise ResourceDoesNotExistError("Order with the given id does not exist")
    await orders.update_status(order_id, new_status, db=db)
    return Message(message=f"The order status updated to {new_status}")
