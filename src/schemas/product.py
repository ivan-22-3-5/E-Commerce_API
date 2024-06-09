from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
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


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
