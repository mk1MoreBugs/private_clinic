import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.security.oauth2_scheme import oauth2_scheme
from database.database import create_db_tables_and_engine

DB_HOST = os.getenv("POSTGRES_SERVER")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
password_file = open(os.getenv("POSTGRES_PASSWORD_FILE"), "r")
DB_PASSWORD = password_file.read()[:-1]
password_file.close()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_db_tables_and_engine(
    database_url=SQLALCHEMY_DATABASE_URL,
)


def session_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(session_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
