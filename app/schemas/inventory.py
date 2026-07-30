from pydantic import BaseModel, Field


class InventoryAdjust(BaseModel):
    sku: str
    delta: int = Field(description="Positive to increase stock, negative to decrease")
