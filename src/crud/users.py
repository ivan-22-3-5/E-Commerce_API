from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import base
from src.db import models
from src.schemas.user import UserIn


async def get_by_email(email: EmailStr, db: AsyncSession) -> models.User | None:
    return await base.get_one(select(models.User).filter(models.User.email == email), db)


async def get_by_id(user_id: int, db: AsyncSession) -> models.User | None:
    return await base.get_one(select(models.User).filter(models.User.id == user_id), db)


async def create(user: UserIn, db: AsyncSession) -> models.User:
    return await base.create(models.User(**user.model_dump()), db)
