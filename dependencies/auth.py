from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from core.security import decode_access_token
from database.dependency import SessionDep
from models.user import User
from repositories.user import get_user_by_id

security = HTTPBearer()


def get_current_user(
    session: SessionDep,
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
) -> User:
    try:
        token = credentials.credentials

        user_id = decode_access_token(token)
        user = get_user_by_id(session, user_id)

    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
