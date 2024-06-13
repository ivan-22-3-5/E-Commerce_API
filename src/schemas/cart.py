from pydantic import BaseModel

from src.schemas.item import Item


class Cart(BaseModel):
    items: list[Item]
    total_price: float
