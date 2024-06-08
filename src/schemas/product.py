from datetime import datetime

from pydantic import BaseModel


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
