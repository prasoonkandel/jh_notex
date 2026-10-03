from database.base import Base
from database.connection import engine
from models.note import Note
from models.user import User


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
