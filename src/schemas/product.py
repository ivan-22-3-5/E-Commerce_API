from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.base import ObjUpdate


class ProductBase(BaseModel):
    title: str
    description: str
    price: float


class ProductIn(ProductBase):
    pass


class ProductOut(BaseModel):
    id: int


class ProductUpdate(ObjUpdate):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)
