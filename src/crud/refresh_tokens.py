from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import base
from src.db import models


async def get_by_user_id(user_id: int, db: AsyncSession) -> models.RefreshToken | None:
    return await base.get_one(select(models.RefreshToken).filter(models.RefreshToken.user_id == user_id), db)


async def add(user_id: int, token: str, db: AsyncSession):
    await base.create(models.RefreshToken(user_id=user_id,
                                          token=token), db)


async def update(user_id: int, new_token: str, db: AsyncSession):
    await base.update_property(select(models.RefreshToken).filter(models.RefreshToken.user_id == user_id),
                               'token', new_token, db)


async def delete(user_id: int, db: AsyncSession):
    await base.delete(select(models.RefreshToken).filter(models.RefreshToken.user_id == user_id), db)
