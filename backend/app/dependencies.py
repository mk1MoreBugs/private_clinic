from sqlalchemy.orm import Session

from database.database import create_db_tables_and_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_db_tables_and_engine(
    database_url=SQLALCHEMY_DATABASE_URL,
)


def session_db():
    with Session(engine) as session:
        yield session
