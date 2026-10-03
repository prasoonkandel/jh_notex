from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.user import User


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="notes")
