from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class OrderItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem]
