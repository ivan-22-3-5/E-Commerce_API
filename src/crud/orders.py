from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.custom_types import OrderStatus
from src.db import models
from src.schemas.order import OrderIn


async def get_by_id(order_id: int, db: AsyncSession) -> models.Order | None:
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    order = result.scalars().first()
    return order


async def create(order: OrderIn, user_id: int, db: AsyncSession) -> models.Order | None:
    new_order = models.Order(
        user_id=user_id,
        **order.model_dump()
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def update_status(order_id: int, new_status: OrderStatus, db: AsyncSession):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    order = result.scalars().first()
    if order:
        order.status = new_status
        await db.commit()
