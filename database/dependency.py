from collections.abc import Generator

from sqlalchemy.orm import Session

from database.connection import engine


def get_session():
    return Session(engine)
