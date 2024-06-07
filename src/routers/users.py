from fastapi import APIRouter, status

from src.crud import users
from src.schemas.user import UserIn, UserOut
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceAlreadyExistError

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user_to_create: UserIn, db: db_dependency):
    if await users.get_by_email(user_to_create.email, db=db):
        raise ResourceAlreadyExistError("Email is already registered")
    await users.create(user_to_create, db=db)
    return {"message": "A new user has been successfully created"}


@router.get('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_me(user: cur_user_dependency):
    return user
