from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.note import create_note
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
    note = create_note(session, current_user, request.title)

    return NoteResponse(id=note.id, title=note.title, content=note.content)
