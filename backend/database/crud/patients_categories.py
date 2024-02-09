from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from ..models.patient_category import PatientCategory


def create_patient_category(session: sessionmaker, category, discount_percentage):
    with session() as session:
        patient_category = PatientCategory(
            name=category,
            discount_percentage=discount_percentage,
        )
        session.add(patient_category)
        session.commit()


def read_patient_categories(session: sessionmaker):
    with session() as session:
        stmt = select(PatientCategory)
        return session.scalars(stmt).all()
