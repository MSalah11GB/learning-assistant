import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.models.user import User


def get_user_by_clerk_id(db: Session, clerk_user_id: str) -> User | None:
    statement = select(User).where(User.clerk_user_id == clerk_user_id)
    return db.scalars(statement).first()


def _fetch_clerk_profile(clerk_user_id: str) -> tuple[str, str | None]:
    """Fetch email and display name for a Clerk user via Clerk's Backend API."""
    settings = get_settings()
    if not settings.clerk_secret_key:
        raise ValueError("Clerk secret key is not configured")

    try:
        response = httpx.get(
            f"https://api.clerk.com/v1/users/{clerk_user_id}",
            headers={"Authorization": f"Bearer {settings.clerk_secret_key}"},
            timeout=5.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise ValueError("Unable to fetch Clerk user profile") from error

    email_addresses = payload.get("email_addresses") or []
    primary_email_id = payload.get("primary_email_address_id")
    primary_email = next(
        (entry.get("email_address") for entry in email_addresses if entry.get("id") == primary_email_id),
        None,
    )
    if not primary_email and email_addresses:
        primary_email = email_addresses[0].get("email_address")
    if not primary_email:
        raise ValueError("Clerk user has no email address on file")

    full_name = " ".join(part for part in (payload.get("first_name"), payload.get("last_name")) if part) or None
    return primary_email, full_name


def get_or_create_user_from_clerk(db: Session, clerk_user_id: str) -> User:
    user = get_user_by_clerk_id(db, clerk_user_id)
    if user is not None:
        return user

    email, full_name = _fetch_clerk_profile(clerk_user_id)
    user = User(clerk_user_id=clerk_user_id, email=email.lower(), full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
