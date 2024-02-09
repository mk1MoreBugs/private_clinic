from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from ..models.diagnosis import Diagnosis


def create_diagnosis(session: sessionmaker, name):
    with session() as session:
        diagnosis = Diagnosis(
            name=name,
        )
        session.add(diagnosis)
        session.commit()


def read_diagnoses(session: sessionmaker):
    with session() as session:
        stmt = select(Diagnosis).order_by(Diagnosis.id)
        return session.scalars(stmt).all()
