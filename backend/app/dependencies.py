from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.security.oauth2_scheme import oauth2_scheme
from database.database import create_db_tables_and_engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./database/sqlite.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"


engine = create_db_tables_and_engine(
    database_url=SQLALCHEMY_DATABASE_URL,
)


def session_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(session_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
