from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.schemas.product import ProductIn, ProductUpdate


async def get_by_id(product_id: int, db: AsyncSession) -> models.Product | None:
    result = await db.execute(select(models.Product).filter(models.Product.id == product_id))
    product = result.scalars().first()
    return product


async def get_all(db: AsyncSession) -> list[models.Product] | None:
    result = await db.execute(select(models.Product))
    return result.scalars().all()


async def create(product: ProductIn, db: AsyncSession) -> models.Product | None:
    new_product = models.Product(
        **product.model_dump()
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def update(product_id: int, product_update: ProductUpdate, db: AsyncSession) -> models.Product | None:
    product = await get_by_id(product_id, db)
    if product:
        for k, v in product_update.model_dump(exclude_none=True).items():
            setattr(product, k, v)
        await db.commit()
        await db.refresh(product)
        return product