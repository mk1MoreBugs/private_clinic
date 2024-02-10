from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import VisitingSession, Patient
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


def read_patient_categories_by_visiting_session_id(session: Session, visiting_session_id):
    stmt = select(
        PatientCategory.discount_percentage
    ).where(
        VisitingSession.id == visiting_session_id
    ).select_from(
        VisitingSession
    ).join(
        Patient, VisitingSession.patient_id == Patient.id
    ).join(
        PatientCategory, PatientCategory.id == Patient.category_id, isouter=True
    ).order_by(
        PatientCategory.discount_percentage.desc()
    )
    return session.scalar(stmt)
