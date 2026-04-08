from fastapi import APIRouter

from app.api.responses import ok
from app.api.schemas.common import ApiResponse
from app.api.schemas.health import HealthData

router = APIRouter()


@router.get("/health", response_model=ApiResponse[HealthData])
def health() -> ApiResponse[HealthData]:
    return ok(HealthData(status="ok"))
