from fastapi import FastAPI
from sqlalchemy import text

import app.models  # noqa: F401
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router
from app.db.base import Base
from app.db.session import engine
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(documents_router)


@app.on_event("startup")
def create_tables() -> None:
    if engine.dialect.name == "postgresql":
        with engine.begin() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Learning Assistant API"}
