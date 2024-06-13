from datetime import datetime

from pydantic import BaseModel

from src.custom_types import OrderStatus
from src.schemas.item import Item, ItemIn


class Order(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime
    user_id: int
    address_id: int


class OrderIn(BaseModel):
    address_id: int
    items: list[ItemIn]


class OrderOut(BaseModel):
    id: int
    address_id: int
    total_price: float
    items: list[Item]
