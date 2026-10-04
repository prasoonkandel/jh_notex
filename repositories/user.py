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


def get_user(session: Session, username: str) -> User:
    existing_user = session.scalar(select(User).where(User.username == username))

    if not existing_user:
        raise ValueError("User does not exist")

    return existing_user


def get_user_by_id(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)

    if not user:
        raise ValueError("User does not exist")

    return user


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

    try:
        session.delete(existing_user)
        session.commit()
        return existing_user
    except:
        session.rollback()
        raise


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

    try:
        session.commit()
        return existing_user
    except:
        session.rollback()
        raise


def change_username(session: Session, old_username: str, new_username: str) -> User:

    existing_user = session.scalar(select(User).where(User.username == old_username))

    if not existing_user:
        raise ValueError("User does not exist")

    existing_user.username = new_username

    try:
        session.commit()
        return existing_user
    except:
        session.rollback()
        raise
