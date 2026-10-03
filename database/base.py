from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database.connection import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str] = mapped_column(String(50))

    notes: Mapped[list["Notes"]] = relationship(back_populates="user")


class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="notes")


Base.metadata.create_all(engine)
