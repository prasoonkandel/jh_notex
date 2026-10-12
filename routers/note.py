from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from database.dependency import SessionDep
from dependencies.auth import get_current_user, security
from models.user import User
from repositories.note import (
    change_title,
    create_note,
    delete_note,
    get_note,
    get_notes,
    get_titles_with_id,
    write_content,
)
from schemas.note import (
    CreateNoteRequest,
    NoteRequest,
    NoteResponse,
    NoteSummary,
    UpdateNoteRequest,
)

router = APIRouter(
    prefix="/api",
    tags=["Notes Operations"],
)

BEARER = Annotated[HTTPAuthorizationCredentials, Depends(security)]

CURRENT_USER = Annotated[User, Depends(get_current_user)]


@router.post("/notes", response_model=NoteResponse)
def create(
    request: CreateNoteRequest,
    current_user: CURRENT_USER,
    session: SessionDep,
):
    try:
        note = create_note(session, current_user, request.title)
        return NoteResponse(id=note.id, title=note.title, content=note.content)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/notes",
    response_model=list[NoteResponse | NoteSummary],
)
def notes(
    current_user: CURRENT_USER,
    session: SessionDep,
    titles_only: bool = False,
):
    if titles_only:
        notes = get_titles_with_id(session, current_user)

        response = []
        for note_id, title in notes:
            response.append(NoteSummary(id=note_id, title=title))

        return response

    return get_notes(session, current_user)


@router.get("/notes/{note_id}", response_model=NoteResponse)
def note(current_user: CURRENT_USER, session: SessionDep, note_id: int):
    try:
        note = get_note(session, current_user, note_id)
        return NoteResponse(id=note.id, title=note.title, content=note.content)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))


@router.patch("/notes")
def write(request: UpdateNoteRequest, current_user: CURRENT_USER, session: SessionDep):
    if request.title is None and request.content is None:
        raise HTTPException(
            status_code=400,
            detail="No update information provided",
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

    return {"message": "Note Updated Successfully!"}


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
