from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.database import create_db_tables_and_engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./database/sqlite.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"


engine = create_db_tables_and_engine(
    database_url=SQLALCHEMY_DATABASE_URL,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def session_db():
    with Session(engine) as session:
        yield session
