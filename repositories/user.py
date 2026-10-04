from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import engine
from models.note import Note
from models.user import User

session = Session(engine)


def create_user(session: Session, username: str, password_hash: str) -> User:
    existing_user = session.scalar(select(User).where(User.username == username))

    if existing_user:
        raise ValueError("User already exists")

    user = User(username=username, password_hash=password_hash)
    try:
        session.add(user)
        session.commit()
    except:
        session.rollback()
        raise

    return user


def delete_user(session: Session, username: str, password_hash: str) -> User:
    existing_user = session.scalar(select(User).where(User.username == username))
    if not existing_user:
        raise ValueError("User does not exist")

    session.delete(existing_user)
    session.commit()
    return existing_user


def user_exists(session: Session, username: str) -> bool:
    exists = session.scalar(select(User).where(User.username == username))
    if not exists:
        return False
    return True
