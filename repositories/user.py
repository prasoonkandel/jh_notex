from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import engine
from models.note import Note
from models.user import User

session = Session(engine)


def user_exists(session: Session, username: str) -> bool:
    exists = session.scalar(select(User).where(User.username == username))
    if not exists:
        return False
    return True


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


def change_password(
    session: Session, username: str, new_password_hash: str, old_password_hash: str
) -> User:
    existing_user = session.scalar(select(User).where(User.username == username))
    if not existing_user:
        raise ValueError("User does not exist")

    if existing_user.password_hash != old_password_hash:
        raise ValueError("Old password is incorrect")

    if old_password_hash == new_password_hash:
        raise ValueError("New password cannot be the same as the old password")

    existing_user.password_hash = new_password_hash

    session.commit()

    return existing_user
