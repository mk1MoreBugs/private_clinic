from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from .models.patient import Patient
from .models.patient_category import PatientCategory


def create_patient_categories(session: sessionmaker, category, discount_percentage):
    with session() as session:
        patient_category = PatientCategory(
            category=category,
            discount_percentage=discount_percentage,
        )
        session.add(patient_category)
        session.commit()


def read_patient_categories(session: sessionmaker):
    with session() as session:
        stmt = select(PatientCategory)
        return session.scalars(stmt).all()


def create_patient(
        session: sessionmaker,
        last_name,
        first_name,
        middle_name,
        birthday,
        category_id=None,
        ):
    with session() as session:

        patient = Patient(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birthday=birthday,
            category_id=category_id,
        )
        session.add(patient)
        session.commit()


def read_patient(session: sessionmaker):
    with session() as session:
        stmt = select(Patient).join(PatientCategory.patients, full=True).order_by(Patient.id)
        return session.scalars(stmt).all()
