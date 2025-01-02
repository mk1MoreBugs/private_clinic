import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.security.oauth2_scheme import oauth2_scheme
from database.create_database_url import create_database_url
from database.database import create_db_tables_and_engine


engine = create_db_tables_and_engine(
    database_url=create_database_url(),
)


def session_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(session_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
