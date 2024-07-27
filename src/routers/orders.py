import stripe
from fastapi import APIRouter, status, Request

from src.config import settings
from src.constraints import admin_path, confirmed_email_required
from src.crud import orders, products, addresses
from src.custom_types import OrderStatus
from src.schemas.client_secret import ClientSecret
from src.schemas.message import Message
from src.schemas.order import OrderIn
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceDoesNotExistError, NotEnoughRightsError

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@confirmed_email_required
@router.post('', status_code=status.HTTP_201_CREATED, response_model=ClientSecret)
async def create_order(user: cur_user_dependency, order: OrderIn, db: db_dependency):
    if (address := await addresses.get_by_id(order.address_id, db)) is None:
        raise ResourceDoesNotExistError("Address with the given id does not exist")
    if address.user_id != user.id:
        raise NotEnoughRightsError("Address does not belong to the user")
    for item in order.items:
        if not await products.get_by_id(item.product_id, db):
            raise ResourceDoesNotExistError("Product with the given id does not exist")
    order = await orders.create(order, user.id, db=db)
    payment_intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100),
        currency="usd",
        automatic_payment_methods={
            "enabled": True
        },
        metadata={
            "order_id": str(order.id)
        },
        api_key=settings.STRIPE_SECRET_KEY
    )
    return ClientSecret(client_secret=payment_intent.client_secret)


@router.post('/{order_id}/cancel', status_code=status.HTTP_200_OK, response_model=Message)
async def cancel_order(order_id: int, user: cur_user_dependency, db: db_dependency):
    if (order := await orders.get_by_id(order_id, db)) is None:
        raise ResourceDoesNotExistError("Order with the given id does not exist")
    if order.user_id != user.id:
        raise NotEnoughRightsError("User is not the order owner")
    await orders.update_status(order_id, OrderStatus.CANCELLED, db=db)
    return Message(message="The order cancelled")


@router.patch('/{order_id}/status', status_code=status.HTTP_200_OK, response_model=Message)
@admin_path
async def change_order_status(user: cur_user_dependency, order_id: int, new_status: OrderStatus, db: db_dependency):
    if not await orders.get_by_id(order_id, db):
        raise ResourceDoesNotExistError("Order with the given id does not exist")
    await orders.update_status(order_id, new_status, db=db)
    return Message(message=f"The order status updated to {new_status.value}")
