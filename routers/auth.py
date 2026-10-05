from fastapi import APIRouter, HTTPException, status

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from database.dependency import SessionDep
from repositories.user import create_user
from schemas.auth import RegisterRequest, TokenResponse

router = APIRouter()


@router.post("/auth/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: SessionDep):
    try:
        user = create_user(db, request.username, hash_password(request.password))

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)
