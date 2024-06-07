from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import models
from src.schemas.user import UserIn
from src.utils import hash_pass


async def get_by_email(email: EmailStr, db: AsyncSession) -> models.User | None:
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalars().first()
    return user


async def get_by_id(user_id: int, db: AsyncSession) -> models.User | None:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    return user


async def create(user: UserIn, db: AsyncSession) -> models.User:
    new_user = models.User(
        email=user.email,
        password=hash_pass(user.password),
        username=user.username,
        created_at=datetime.now()
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
