from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from src.custom_types import OrderStatus


class Order(BaseModel):
    id: int
    status: Literal[
        OrderStatus.PENDING,
        OrderStatus.SHIPPED,
        OrderStatus.CONFIRMED,
        OrderStatus.DELIVERED,
        OrderStatus.CANCELLED
    ]
    created_at: datetime
    user_id: int
    product_id: int


class OrderIn(BaseModel):
    product_id: int


class OrderOut(BaseModel):
    id: int
    product_id: int
