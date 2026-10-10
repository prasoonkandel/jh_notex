from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm.session import Session

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    password_hash,
    verify_password,
)
from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.user import change_password, change_username
from schemas.user import ChangePasswordRequest, ChangeUsernameRequest, UserResponse

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


@router.post("/password")
def password(
    request: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
):
    if not verify_password(request.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old Password is Incorrect",
        )

    if verify_password(request.new_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="New Password can not be same as Old Password",
        )

    try:
        change_password(
            session,
            current_user.username,
            hash_password(request.new_password),
        )

        return {"message": "Password Changed Succesfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/change-username")
def username(
    request: ChangeUsernameRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
):
    try:
        change_username(session, current_user.username, request.new_username)
        return {"message": "Username Changed Succesfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
