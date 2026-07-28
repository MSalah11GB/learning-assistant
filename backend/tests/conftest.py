import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ.setdefault("CLERK_ISSUER", "https://test.clerk.accounts.dev")
os.environ.setdefault("CLERK_SECRET_KEY", "test-secret-key")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.models.user import User


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session(reset_database: None) -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def make_user(db_session: Session):
    def _make_user(clerk_user_id: str, email: str, full_name: str | None = None) -> User:
        user = User(clerk_user_id=clerk_user_id, email=email, full_name=full_name)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _make_user


@pytest.fixture
def authed_user(make_user) -> User:
    return make_user("user_test123", "student@example.com", "Study Student")


@pytest.fixture
def authed_client(client: TestClient, authed_user: User) -> TestClient:
    app.dependency_overrides[get_current_user] = lambda: authed_user
    return client
