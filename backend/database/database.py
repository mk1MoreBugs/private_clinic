from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"


def create_db(database_url=SQLALCHEMY_DATABASE_URL, echo=False):
    engine = create_engine(database_url, echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(engine)
