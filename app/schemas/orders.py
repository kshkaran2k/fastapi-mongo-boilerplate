from typing import List

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem]
