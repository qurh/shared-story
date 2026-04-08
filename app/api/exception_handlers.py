from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.schemas.common import ApiError, ApiResponse


def _status_to_code(status_code: int) -> str:
    mapping = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
    }
    return mapping.get(status_code, f"HTTP_{status_code}")


def _error_payload(*, code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return ApiResponse(
        success=False,
        data=None,
        error=ApiError(code=code, message=message, details=details),
    ).model_dump()


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        details = exc.detail if isinstance(exc.detail, dict) else None
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(code=_status_to_code(exc.status_code), message=message, details=details),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_payload(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                details={"errors": exc.errors()},
            ),
        )

