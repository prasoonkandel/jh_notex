from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    notes: Mapped[list["Note"]] = relationship(back_populates="user")
