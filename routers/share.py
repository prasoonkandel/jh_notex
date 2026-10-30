import secrets
import string
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError

from database.dependency import SessionDep
from dependencies.auth import get_current_user
from models.user import User
from repositories.note import get_note
from repositories.share import create_share, delete_shares, get_shared_note
from schemas.note import NoteResponse
from schemas.share import ShareResponse

router = APIRouter(
    prefix="/api",
    tags=["Share Operations"],
)

SHARE_CODE_ALPHABET = string.ascii_letters + string.digits
SHARE_CODE_LENGTH = 7
SHARE_CODE_ATTEMPTS = 10

CURRENT_USER = Annotated[User, Depends(get_current_user)]


@router.post(
    "/notes/{note_id}/share",
    response_model=ShareResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    note_id: int,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    try:
        get_note(session, current_user, note_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    for _ in range(SHARE_CODE_ATTEMPTS):
        share_code = "".join(
            secrets.choice(SHARE_CODE_ALPHABET) for _ in range(SHARE_CODE_LENGTH)
        )
        try:
            share = create_share(session, note_id, share_code)
            return ShareResponse(share_code=share.share_code)
        except ValueError as e:
            if str(e) != "Share already exists":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=str(e),
                )
        except IntegrityError:
            continue

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Unable to generate a unique share code",
    )


@router.get("/share/{share_code}", response_model=NoteResponse)
def get_shared(
    session: SessionDep,
    share_code: str = Path(
        ...,
        min_length=SHARE_CODE_LENGTH,
        max_length=SHARE_CODE_LENGTH,
        pattern=r"^[A-Za-z0-9]+$",
    ),
):
    try:
        note = get_shared_note(session, share_code)
        return NoteResponse(id=note.id, title=note.title, content=note.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/notes/{note_id}/share")
def revoke(
    note_id: int,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    try:
        get_note(session, current_user, note_id)
        count = delete_shares(session, note_id)
        return {"message": "Shares revoked successfully", "count": count}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
