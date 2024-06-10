from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import base
from src.db import models
from src.schemas.address import AddressIn, AddressUpdate


async def get_by_id(address_id: str, db: AsyncSession) -> models.Address | None:
    return await base.get_one(select(models.Address).filter(models.Address.id == address_id), db)


async def create(user_id: int, address: AddressIn, db: AsyncSession) -> models.Address | None:
    return await base.create(models.Address(
        user_id=user_id,
        **address.model_dump()
    ), db)


async def update(address_id: int, address_update: AddressUpdate, db: AsyncSession) -> models.Address | None:
    return await base.update(select(models.Address).filter(models.Address.id == address_id), address_update, db)


async def delete(address_id: str, db: AsyncSession):
    await base.delete(select(models.Address).filter(models.Address.id == address_id), db)
