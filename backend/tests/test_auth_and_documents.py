from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app
from app.models.user import User


def test_me_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_rejects_an_invalid_bearer_token(client: TestClient) -> None:
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_me_returns_the_current_user(authed_client: TestClient, authed_user: User) -> None:
    response = authed_client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == authed_user.email


def test_documents_require_authentication(client: TestClient) -> None:
    response = client.get("/api/documents")
    assert response.status_code == 401


def test_documents_validation_rejects_a_missing_title(authed_client: TestClient) -> None:
    response = authed_client.post("/api/documents", json={"content": "Notes about retrieval."})
    assert response.status_code == 422


def test_documents_are_scoped_to_the_authenticated_user(client: TestClient, make_user) -> None:
    first_user = make_user("user_first", "first@example.com")
    second_user = make_user("user_second", "second@example.com")

    app.dependency_overrides[get_current_user] = lambda: first_user
    create_response = client.post("/api/documents", json={"title": "Lecture 1", "content": "Notes about retrieval."})
    assert create_response.status_code == 201

    first_documents = client.get("/api/documents")
    assert [document["title"] for document in first_documents.json()] == ["Lecture 1"]

    app.dependency_overrides[get_current_user] = lambda: second_user
    second_documents = client.get("/api/documents")
    assert second_documents.json() == []
