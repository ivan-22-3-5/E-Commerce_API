from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class ItemIn(ItemBase):
    pass


class ItemOut(ItemBase):
    total_price: float
