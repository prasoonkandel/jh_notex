from collections.abc import Generator

from sqlalchemy.orm import Session

from database.connection import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
