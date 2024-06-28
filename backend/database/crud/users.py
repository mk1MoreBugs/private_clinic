from sqlalchemy.orm import Session

from database.models.user import User
from sqlalchemy import select
from sqlalchemy import update

from database.models.user import User


def create_user_and_flush(
        session: Session,
        last_name: str,
        first_name: str,
        hashed_password: str,
        middle_name: str | None = None,
):
    user = User(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        hashed_password=hashed_password,
    )

    session.add(user)
    session.flush()
    return user


def create_user_and_commit(
        session: Session,
        last_name: str,
        first_name: str,
        hashed_password: str,
        middle_name: str | None = None,
):
    user = create_user_and_flush(
        session=session,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        hashed_password=hashed_password,
    )
    session.commit()


def read_users(session: Session):
    stmt = select(
        User
    ).select_from(
        User
    )

    return session.execute(stmt).scalars().all()
