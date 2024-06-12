from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.crud import base, products
from src.db import models
from src.schemas.cart import CartItem, CartItemIn


async def get_by_user(user_id: int, db: AsyncSession) -> models.Cart | None:
    return await base.get_one(select(models.Cart).
                              filter(models.Cart.user_id == user_id).
                              options(joinedload(models.Cart.items)), db)


async def add_item(user_id: int, item: CartItemIn, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart and await products.get_by_id(item.product_id, db):
        existing_item = next((i for i in cart.items if i.product_id == item.product_id), None)
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            new_item = models.CartItem(**item.model_dump(), cart_id=cart.id)
            cart.items.append(new_item)
        await db.commit()
        await db.refresh(cart)
        return cart


async def remove_item(user_id: int, item: CartItemIn, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart:
        existing_item = next((i for i in cart.items if i.product_id == item.product_id), None)
        if existing_item:
            if existing_item.quantity <= item.quantity:
                await db.delete(existing_item)
            else:
                existing_item.quantity -= item.quantity
        await db.commit()
        await db.refresh(cart)
        return cart


async def clear(user_id: int, db: AsyncSession) -> models.Cart | None:
    cart = await get_by_user(user_id, db)
    if cart:
        cart.items = []
        await db.commit()
        await db.refresh(cart)
        return cart
