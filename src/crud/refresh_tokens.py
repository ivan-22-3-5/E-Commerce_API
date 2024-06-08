from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models


async def get_by_user_id(user_id: int, db: AsyncSession) -> models.RefreshToken | None:
    result = await db.execute(select(models.RefreshToken).filter(models.RefreshToken.user_id == user_id))
    refresh_token = result.scalars().first()
    return refresh_token


async def add_token(user_id: int, token: str, db: AsyncSession):
    new_token = models.RefreshToken(user_id=user_id,
                                    token=token)
    db.add(new_token)
    await db.commit()


async def update_token(user_id: int, new_token: str, db: AsyncSession):
    result = await db.execute(select(models.RefreshToken).filter(models.RefreshToken.user_id ==user_id))
    db_token = result.scalars().first()
    if db_token:
        db_token.token = new_token
        await db.commit()


async def delete_token(user_id: int, db: AsyncSession):
    token = await get_by_user_id(user_id, db)
    if token:
        await db.delete(token)
        await db.commit()
