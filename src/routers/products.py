from fastapi import APIRouter, status

from src.crud import products
from src.custom_exceptions import NotEnoughRightsError
from src.deps import db_dependency, cur_user_dependency
from src.schemas.product import ProductIn, ProductOut

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(product: ProductIn, user: cur_user_dependency, db: db_dependency):
    if not user.is_admin:
        raise NotEnoughRightsError("Only admin user can access this endpoint")
    return await products.create(product, db=db)
