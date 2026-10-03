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


def change_password(username: str, old_password: str, new_password: str) -> User:
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password == old_password:
            user.password = new_password
            session.commit()
            return user
    return None


Base.metadata.create_all(engine)


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    if add_user(username, password):
        print("User added successfully.")
    else:
        print("Failed to add user.")

    print("================================")
    username = input("Username: ")
    password = input("Old Password: ")
    new_password = input("New password: ")
    if change_password(username, password, new_password):
        print("Password changed successfully.")
    else:
        print("Username or password is incorrect.")
