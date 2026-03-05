from typing import Any, Literal

from pydantic import BaseModel, Field


class Page(BaseModel):
    totalPages: int = Field(ge=0)
    currentPage: int = Field(ge=1)
    limit: int = Field(ge=1)
    totalRecords: int = Field(ge=0)


class APIResponse(BaseModel):
    status: Literal["Success", "Failed"]
    message: str
    data: dict[str, Any] | list[Any] | None = None
    page: Page | None = None
    warnings: str | None = None
    statusCode: Literal[200, 400, 422, 500]


async def success_response(
    message: str = "Request successful",
    data: dict[str, Any] | list[Any] | None = None,
    page: Page | None = None,
    warnings: str | None = None,
) -> APIResponse:
    return APIResponse(
        status="Success",
        message=message,
        data=data,
        page=page,
        warnings=warnings,
        statusCode=200,
    )


async def failure_response(
    *,
    status_code: Literal[400, 422, 500],
    message: str,
    data: dict[str, Any] | list[Any] | None = None,
    warnings: str | None = None,
    page: Page | None = None,
) -> APIResponse:
    return APIResponse(
        status="Failed",
        message=message,
        data=data,
        page=page,
        warnings=warnings,
        statusCode=status_code,
    )
