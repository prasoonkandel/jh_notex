from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_409_CONFLICT

from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.note import create_note, write_content
from schemas.note import (
    ChangeTitleRequest,
    CreateNoteRequest,
    DeleteNoteRequest,
    NoteRequest,
    NoteResponse,
    WriteContentRequest,
)

router = APIRouter(
    prefix="/api/note",
    tags=["Note Operations"],
)

BEARER = Annotated[HTTPAuthorizationCredentials, Depends(security)]

CURRENT_USER = Annotated[User, Depends(get_current_user)]


@router.post("/create")
def create(
    request: CreateNoteRequest,
    current_user: CURRENT_USER,
    session: SessionDep,
    response_model=NoteResponse,
):
    try:
        note = create_note(session, current_user, request.title)
        return NoteResponse(id=note.id, title=note.title, content=note.content)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.post("/write")
def write(
    request: WriteContentRequest, current_user: CURRENT_USER, session: SessionDep
):
    try:
        write_content(session, current_user, request.id, request.content)
        return {"message": "Note written and saved sucessfully!"}
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
