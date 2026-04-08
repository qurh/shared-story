from typing import Any

from fastapi.responses import JSONResponse

from app.api.schemas.common import ApiError, ApiResponse


def ok(data: Any) -> ApiResponse[Any]:
    return ApiResponse(success=True, data=data, error=None)


def fail(
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    data: Any = None,
) -> JSONResponse:
    payload = ApiResponse(
        success=False,
        data=data,
        error=ApiError(code=code, message=message, details=details),
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())

