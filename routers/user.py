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
from models.user import User
from repositories.user import create_user, get_user
from schemas.user import UserResponse

router = APIRouter(
    prefix="/api/user",
    tags=["User Operations"],
)


BEARER = Annotated[
    HTTPAuthorizationCredentials,
    Depends(security),
]


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return UserResponse(id=current_user.id, username=current_user.username)
