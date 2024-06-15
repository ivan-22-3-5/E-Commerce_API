from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.base import ObjUpdate


class ProductBase(BaseModel):
    title: str
    description: str
    full_price: float


class ProductIn(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    rating: float
    final_price: float


class ProductUpdate(ObjUpdate):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    full_price: Optional[float] = Field(default=None)
    discount: Optional[float] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)
