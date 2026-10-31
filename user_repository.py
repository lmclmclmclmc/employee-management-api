from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User


def get_user_by_username(
    session: Session,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)

    return session.scalar(statement)


def create_user(
    session: Session,
    username: str,
    password_hash: str,
) -> User | None:
    user = User(
        username=username,
        password_hash=password_hash,
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None

    session.refresh(user)

    return user
