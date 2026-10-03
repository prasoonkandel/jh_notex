from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session

from database.connection import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))


def add_user(username: str, password: str) -> User:
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return user
    return user


Base.metadata.create_all(engine)


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    add_user(username, password)
