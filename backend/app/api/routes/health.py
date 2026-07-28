from fastapi import APIRouter

from app.schemas.system import HealthResponse, PingResponse
from app.services.system_service import get_health_payload, get_ping_payload

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    payload = get_health_payload()
    return HealthResponse(
        status=payload.status,
        service=payload.service,
        detail=payload.detail,
    )


@router.get("/api/ping", response_model=PingResponse)
async def ping() -> PingResponse:
    payload = get_ping_payload()
    return PingResponse(message=payload.message, backend=payload.backend)
