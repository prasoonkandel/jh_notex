from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from repositories.user import create_user, get_user
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse

router = APIRouter(
    prefix="/api/user",
    tags=["User Operations"],
)


BEARER = Annotated[
    HTTPAuthorizationCredentials,
    Depends(security),
]


@router.post("/me", response_model=UserResponse)
def get_me(
    credentials: BEARER,
    db: SessionDep,
):
    current_user = get_current_user(session=db, credentials=credentials)
    return UserResponse(id=current_user.id, username=current_user.username)
