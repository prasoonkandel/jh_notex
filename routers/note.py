from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.note import change_title, create_note, delete_note, write_content
from schemas.note import CreateNoteRequest, NoteRequest, NoteResponse, UpdateNoteRequest

router = APIRouter(
    prefix="/api",
    tags=["Notes Operations"],
)

BEARER = Annotated[HTTPAuthorizationCredentials, Depends(security)]

CURRENT_USER = Annotated[User, Depends(get_current_user)]


@router.post("/notes")
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


@router.patch("/notes")
def write(request: UpdateNoteRequest, current_user: CURRENT_USER, session: SessionDep):
    if not request.title or request.content:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="No Updation Information Provided"
        )
    if request.title:
        try:
            change_title(session, current_user, request.id, request.title)
        except ValueError as e:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))

    if request.content:
        try:
            write_content(session, current_user, request.id, request.content)
        except ValueError as e:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.delete("/notes/{note_id}")
def delete(
    note_id: int,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    try:
        delete_note(session, current_user, note_id)
        return {"message": "User Deleted Successfully"}
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
