from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.base import ObjUpdate


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    enabled: bool
    created_at: datetime


class ProductIn(BaseModel):
    title: str
    description: str
    price: float


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: float


class ProductUpdate(ObjUpdate):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    enabled: Optional[bool] = Field(default=None)
