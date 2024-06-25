from sqlalchemy.orm import Session

from database.models.user import User


def create_user(
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
