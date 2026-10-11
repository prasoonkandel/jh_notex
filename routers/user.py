from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_400_BAD_REQUEST

from core.security import (
    hash_password,
    password_hash,
    verify_password,
)
from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.user import change_password, change_username, delete_user
from schemas.user import (
    DeleteUserRequest,
    UpdatePasswordRequest,
    UpdateUserRequest,
    UserResponse,
)

router = APIRouter(
    prefix="/api/user",
    tags=["User Operations"],
)


BEARER = Annotated[
    HTTPAuthorizationCredentials,
    Depends(security),
]

CURRENT_USER = Annotated[User, Depends(get_current_user)]


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: CURRENT_USER,
):
    return UserResponse(id=current_user.id, username=current_user.username)


@router.patch("/password")
def password(
    request: UpdatePasswordRequest,
    current_user: CURRENT_USER,
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


@router.patch("/me")
def username(
    request: UpdateUserRequest,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    username_update = bool(request.new_username)

    if not username_update:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No Updation Information Provided"
        )

    if username_update:
        assert request.new_username is not None
        try:
            change_username(session, current_user.username, request.new_username)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )

    return {"message": "User Information Updated!"}


@router.delete("/me")
def delete(
    request: DeleteUserRequest,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password"
        )

    try:
        delete_user(session, current_user.username)
        return {"message": "User Deleted Succesfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
