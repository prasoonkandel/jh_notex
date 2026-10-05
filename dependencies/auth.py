from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from core.security import decode_access_token
from database.dependency import SessionDep
from models.user import User
from repositories.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    session: SessionDep,
    bearer: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        user_id = decode_access_token(bearer)
        user = get_user_by_id(session, user_id)

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
