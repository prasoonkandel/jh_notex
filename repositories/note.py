from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import engine
from models.note import Note
from models.user import User

session = Session(engine)


def create_note(user: User, title: str, content: str) -> Note:
    note = Note(user_id=user.id, title=title, content=content)
    session.add(note)
    session.commit()
    return note
