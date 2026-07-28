from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    detail: str | None = None


class PingResponse(BaseModel):
    message: str
    backend: str
