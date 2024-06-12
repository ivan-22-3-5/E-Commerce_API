from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.crud import base, products
from src.db import models
from src.schemas.cart import CartItemIn


async def get_by_user(user_id: int, db: AsyncSession) -> models.Cart | None:
    return await base.get_one(select(models.Cart).
                              filter(models.Cart.user_id == user_id).
                              options(joinedload(models.Cart.items)), db)


async def add_item(user_id: int, item: CartItemIn, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart and await products.get_by_id(item.product_id, db):
        cart.add_item(**item.model_dump())
        await db.commit()
        await db.refresh(cart)
        return cart


async def remove_item(user_id: int, item: CartItemIn, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart:
        cart.remove_item(**item.model_dump())
        await db.commit()
        await db.refresh(cart)
        return cart


async def clear(user_id: int, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart:
        cart.clear()
        await db.commit()
        await db.refresh(cart)
        return cart
