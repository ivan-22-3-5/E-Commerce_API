from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import base
from src.db import models
from src.schemas.user import UserIn
from src.utils import hash_pass


async def get_by_email(email: EmailStr, db: AsyncSession) -> models.User | None:
    return await base.get_one(select(models.User).filter(models.User.email == email), db)


async def get_by_id(user_id: int, db: AsyncSession) -> models.User | None:
    return await base.get_one(select(models.User).filter(models.User.id == user_id), db)


async def create(user: UserIn, db: AsyncSession) -> models.User:
    new_user = models.User(
        **user.model_dump(exclude={'password'}),
        password=hash_pass(user.password),
    )
    new_user.cart = models.Cart(user_id=new_user.id)
    return await base.create(new_user, db)
