from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.patient_category import PatientCategory


def create_patient_category(session: Session, category, discount_percentage):
    patient_category = PatientCategory(
        name=category,
        discount_percentage=discount_percentage,
    )
    session.add(patient_category)
    session.commit()


def read_patient_categories(session: Session):
    stmt = select(PatientCategory)
    return session.scalars(stmt).all()
