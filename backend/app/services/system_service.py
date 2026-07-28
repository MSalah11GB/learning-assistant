from dataclasses import dataclass


@dataclass(frozen=True)
class HealthPayload:
    status: str
    service: str
    detail: str | None = None


@dataclass(frozen=True)
class PingPayload:
    message: str
    backend: str


def get_health_payload() -> HealthPayload:
    return HealthPayload(status="ok", service="backend", detail="ready")


def get_ping_payload() -> PingPayload:
    return PingPayload(message="pong", backend="healthy")
