from database.models.base import Base


def test_create_table(db_session):
    assert len(Base.metadata.tables.keys()) == 10  # number of tables
