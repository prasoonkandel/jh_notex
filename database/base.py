from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database.connection import engine


class Base(DeclarativeBase):
    pass
