from fastapi import APIRouter, status

from src.constraints import admin_path
from src.crud import products
from src.deps import db_dependency, cur_user_dependency
from src.schemas.product import ProductIn, ProductOut

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=ProductOut)
@admin_path
async def create_product(product: ProductIn, db: db_dependency, user: cur_user_dependency):
    return await products.create(product, db=db)


@router.get('', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def get_all_products(db: db_dependency):
    return await products.get_all(db=db)
