from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class Item(BaseModel):
    product_id: int
    quantity: int
    total_price: float
