from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from models.note import Note
from models.user import User


def create_note(session: Session, user: User, title: str, content: str) -> Note:

    note = Note(user_id=user.id, title=title, content=content)
    try:
        session.add(note)
        session.commit()
        return note
    except:
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

    notes_list = []

    for note in notes:
        notes_list.append(note)

    return notes_list


def delete_note(session: Session, user: User, note_id: int) -> None:

    try:
        session.execute(delete(Note).where(Note.id == note_id, Note.user_id == user.id))
        session.commit()
    except:
        session.rollback()
        raise


def delete_notes(session: Session, user: User) -> None:

    try:
        session.execute(delete(Note).where(Note.user_id == user.id))
        session.commit()
    except:
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


def write_note(
    session: Session, user: User, note_id: int, title: str, content: str
) -> Note:

    note = session.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.user_id == user.id,
        )
    )

    if not note:
        raise ValueError("Note does not exist")

    note.title = title
    note.content = content
    try:
        session.commit()
        return note
    except:
        session.rollback()
        raise
