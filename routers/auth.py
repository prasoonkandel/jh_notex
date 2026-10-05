from fastapi import APIRouter, HTTPException, status

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from database.dependency import SessionDep
from repositories.user import create_user, get_user
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse, User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse)
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


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: SessionDep):

    user = get_user(db, request.username)

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
        )

    access_token = create_access_token(user.id)

    return TokenResponse(access_token=access_token)


@router.post("/me", response_model=User)
def get_user(db: SessionDep, token: str):
    user_id = decode_access_token(token)
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return User(id=user.id, username=user.username)
