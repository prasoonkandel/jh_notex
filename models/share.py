from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.note import Note


class Share(Base):
    __tablename__ = "shares"

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    share_code: Mapped[str] = mapped_column(String(7), primary_key=True)
    note: Mapped["Note"] = relationship(back_populates="shares")
