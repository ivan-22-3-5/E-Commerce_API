from fastapi import APIRouter, status

from src.crud import users
from src.schemas.order import OrderOut
from src.schemas.user import UserIn, UserOut
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceAlreadyExistError

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserIn, db: db_dependency):
    if await users.get_by_email(user.email, db=db):
        raise ResourceAlreadyExistError("Email is already registered")
    return await users.create(user, db=db)


@router.get('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_me(user: cur_user_dependency):
    return user


@router.get('/me/orders', response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_my_orders(user: cur_user_dependency, db: db_dependency):
    return await users.get_orders_by_user_id(user.id, db)
