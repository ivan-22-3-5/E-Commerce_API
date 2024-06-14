from typing import Optional

from fastapi import APIRouter, status

from src.crud import users, orders, reviews, carts
from src.schemas.cart import CartOut
from src.schemas.item import ItemIn
from src.schemas.order import OrderOut
from src.schemas.review import ReviewOut
from src.schemas.user import UserIn, UserOut
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceAlreadyExistsError

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserIn, db: db_dependency):
    if await users.get_by_email(user.email, db=db):
        raise ResourceAlreadyExistsError("Email is already registered")
    return await users.create(user, db=db)


@router.get('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_me(user: cur_user_dependency):
    return user


@router.get('/me/orders', response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_my_orders(user: cur_user_dependency, db: db_dependency):
    return await orders.get_by_user(user.id, db)


@router.get('/me/reviews', response_model=list[ReviewOut], status_code=status.HTTP_200_OK)
async def get_my_reviews(user: cur_user_dependency, db: db_dependency):
    return await reviews.get_by_user(user.id, db)


@router.get('/me/cart', response_model=CartOut, status_code=status.HTTP_200_OK)
async def get_my_cart(user: cur_user_dependency, db: db_dependency):
    return await carts.get_by_user(user.id, db)


@router.post('/me/cart/items', response_model=Optional[CartOut], status_code=status.HTTP_200_OK)
async def add_item_to_cart(user: cur_user_dependency, item: ItemIn, db: db_dependency):
    return await carts.add_item(user.id, item, db)


@router.delete('/me/cart/items', response_model=Optional[CartOut], status_code=status.HTTP_200_OK)
async def remove_item_from_cart(user: cur_user_dependency, item: ItemIn, db: db_dependency):
    return await carts.remove_item(user.id, item, db)


@router.post('/me/cart/clear', response_model=CartOut, status_code=status.HTTP_200_OK)
async def clear_cart(user: cur_user_dependency, db: db_dependency):
    return await carts.clear(user.id, db)

