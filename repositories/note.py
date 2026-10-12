from typing import Any, cast

from sqlalchemy import delete, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Session

from models.note import Note
from models.user import User


def create_note(session: Session, user: User, title: str) -> Note:

    note = Note(user_id=user.id, title=title, content="")
    try:
        session.add(note)
        session.commit()
        return note
    except Exception:
        session.rollback()
        raise


def get_note(session: Session, user: User, note_id: int) -> Note:

    note = session.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id,
        )
    )

    if note is None:
        raise ValueError("Note does not exist")

    return note


def get_notes(session: Session, user: User) -> list[Note]:
    notes = session.scalars(select(Note).where(Note.user_id == user.id)).all()
    return list(notes)


def delete_note(session: Session, user: User, note_id: int) -> None:

    try:
        result = cast(
            CursorResult[Any],
            session.execute(
                delete(Note).where(Note.id == note_id, Note.user_id == user.id)
            ),
        )

        if result.rowcount == 0:
            raise ValueError("Note does not exist")

        session.commit()
    except Exception:
        session.rollback()
        raise


def delete_notes(session: Session, user: User) -> int:
    try:
        result = cast(
            CursorResult[Any],
            session.execute(delete(Note).where(Note.user_id == user.id)),
        )

        count = result.rowcount
        session.commit()
        return count
    except Exception:
        session.rollback()
        raise


def get_titles_with_id(session: Session, user: User) -> list[tuple[int, str]]:

    titles_with_id = session.execute(
        select(Note.id, Note.title).where(Note.user_id == user.id)
    ).all()

    title_id_tuples = []
    for note_id, title in titles_with_id:
        title_id_tuples.append((note_id, title))

    return title_id_tuples


def write_content(session: Session, user: User, note_id: int, content: str) -> Note:

    note = session.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id,
        )
    )

    if not note:
        raise ValueError("Note does not exist")

    note.content = content

    try:
        session.commit()
        return note
    except Exception:
        session.rollback()
        raise


def change_title(session: Session, user: User, note_id: int, title: str) -> Note:
    note = session.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id,
        )
    )

    if not note:
        raise ValueError("Note does not exist")

    note.title = title

    try:
        session.commit()
        return note

    except Exception as e:
        session.rollback()
        raise
