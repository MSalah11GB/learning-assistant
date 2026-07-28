from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.auth import UserRead

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me", response_model=UserRead)
def me(current_user=Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
