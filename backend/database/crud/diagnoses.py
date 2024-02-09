from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.diagnosis import Diagnosis


def create_diagnosis(session: Session, name: str):
    diagnosis = Diagnosis(
        name=name,
    )
    session.add(diagnosis)
    session.commit()


def read_diagnoses(session: Session):
    stmt = select(Diagnosis).order_by(Diagnosis.id)
    return session.scalars(stmt).all()
