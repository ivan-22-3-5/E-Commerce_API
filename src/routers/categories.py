from fastapi import APIRouter, status

from src.constraints import admin_path
from src.crud import categories
from src.schemas.category import CategoryIn
from src.schemas.message import Message
from src.deps import cur_user_dependency, db_dependency
from src.custom_exceptions import ResourceAlreadyExistsError, ResourceDoesNotExistError

router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Message)
@admin_path
async def create_category(user: cur_user_dependency, category: CategoryIn, db: db_dependency):
    if await categories.get_by_name(category.name, db):
        raise ResourceAlreadyExistsError("Category with the given name already exists")
    await categories.create(category, db=db)
    return Message(message=f"Category {category.name} has been successfully created")


@router.delete('/{category_name}', status_code=status.HTTP_200_OK, response_model=Message)
@admin_path
async def delete_category(user: cur_user_dependency, category_name: str, db: db_dependency):
    if not await categories.get_by_name(category_name, db):
        raise ResourceDoesNotExistError("Category with the given name does not exist")
    await categories.delete(category_name, db)
    return Message(message=f"Category {category_name} has been successfully deleted")
