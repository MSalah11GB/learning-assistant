from unittest.mock import Mock, patch

from sqlalchemy.orm import Session

from app.services.auth_service import get_or_create_user_from_clerk


def _clerk_profile_response() -> dict:
    return {
        "id": "user_abc123",
        "email_addresses": [{"id": "idn_1", "email_address": "student@example.com"}],
        "primary_email_address_id": "idn_1",
        "first_name": "Study",
        "last_name": "Student",
    }


def _mock_response(payload: dict) -> Mock:
    response = Mock()
    response.raise_for_status = Mock()
    response.json = Mock(return_value=payload)
    return response


def test_get_or_create_user_from_clerk_provisions_a_new_user(db_session: Session) -> None:
    with patch("app.services.auth_service.httpx.get", return_value=_mock_response(_clerk_profile_response())):
        user = get_or_create_user_from_clerk(db_session, "user_abc123")

    assert user.clerk_user_id == "user_abc123"
    assert user.email == "student@example.com"
    assert user.full_name == "Study Student"


def test_get_or_create_user_from_clerk_reuses_an_existing_user(db_session: Session) -> None:
    mocked_get = patch("app.services.auth_service.httpx.get", return_value=_mock_response(_clerk_profile_response()))

    with mocked_get as mock_get:
        first = get_or_create_user_from_clerk(db_session, "user_abc123")
        second = get_or_create_user_from_clerk(db_session, "user_abc123")

    assert first.id == second.id
    mock_get.assert_called_once()
