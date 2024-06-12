from pydantic import BaseModel, Field


class CartItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CartItem(BaseModel):
    product_id: int
    quantity: int
    total_price: float


class Cart(BaseModel):
    items: list[CartItem]
    total_price: float
