from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import base
from src.db import models


async def get_by_user_id(user_id: int, db: AsyncSession) -> models.RecoveryToken | None:
    return await base.get_one(select(models.RecoveryToken).filter(models.RecoveryToken.user_id == user_id), db)


async def add(user_id: int, token: str, db: AsyncSession):
    await base.create(models.RecoveryToken(user_id=user_id,
                                           token=token), db)


async def update(user_id: int, new_token: str, db: AsyncSession):
    await base.update_property(select(models.RecoveryToken).filter(models.RecoveryToken.user_id == user_id),
                               'token', new_token, db)


async def delete(user_id: int, db: AsyncSession):
    await base.delete(select(models.RecoveryToken).filter(models.RecoveryToken.user_id == user_id), db)
