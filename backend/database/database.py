from sqlalchemy import create_engine

from database.models.base import Base


def create_db_tables_and_engine(database_url, echo=False):
    engine = create_engine(database_url, echo=echo)
    Base.metadata.create_all(engine)
    return engine


def get_metadata():
    return Base.metadata
