from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import engine
from models.note import Note
from models.user import User
from repositories.user import user_exists

session = Session(engine)


def create_note(user: User, title: str, content: str) -> Note:
    note = Note(user_id=user.id, title=title, content=content)
    session.add(note)
    session.commit()
    return note


def get_note(user: User, note_id: int) -> Note:

    if not user_exists(session, user.username):
        raise ValueError("User does not exist")

    note = session.scalar(select(Note).where(Note.id == note_id))

    if note is None:
        raise ValueError("Note does not exist")

    if note.user_id != user.id:
        raise ValueError("Note does not belong to user")

    return note


def get_all_notes(user: User) -> list[Note]:

    if not user_exists(session, user.username):
        raise ValueError("User does not exist")

    notes = session.scalars(select(Note).where(Note.user_id == user.id)).all()

    if not notes:
        raise ValueError("No notes found")

    return notes


def delete_note(user: User, note_id: int) -> None:

    if not user_exists(session, user.username):
        raise ValueError("User does not exist")

    note = session.scalars(select(Note).where(Note.id == note_id))

    if not note:
        raise ValueError("Note does not exist")

    if note.user_id != user.id:
        raise ValueError("Note does not belong to user")

    session.delete(note)
    session.commit()
