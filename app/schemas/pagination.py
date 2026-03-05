from pydantic import BaseModel, Field
from typing import Literal


class PaginationParams(BaseModel):
    limit: int = Field(default=10, ge=1)
    currentPage: int = Field(default=1, ge=1)
    sortByField: str = Field(default="createdDate", min_length=1)
    sortByOrder: Literal["asc", "desc"] = "asc"
