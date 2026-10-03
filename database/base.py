from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database.connection import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    notes: Mapped[list["Note"]] = relationship(back_populates="user")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="notes")


Base.metadata.create_all(engine)
