from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from .models.diagnosis import Diagnosis
from .models.doctor_category import Category
from .models.doctor_speciality import Speciality
from .models.patient import Patient
from .models.patient_category import PatientCategory
from .models.service import Service
from .models.visiting_session import VisitingSession


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


def create_doctor_speciality(session: sessionmaker, name):
    with session() as session:
        doctor_speciality = Speciality(
            name=name,
        )
        session.add(doctor_speciality)
        session.commit()


def read_doctor_speciality(session: sessionmaker):
    with session() as session:
        stmt = select(Speciality).order_by(Speciality.id)
        return session.scalars(stmt).all()


def create_doctor_category(session: sessionmaker, name):
    with session() as session:
        doctor_category = Category(name=name)
        session.add(doctor_category)
        session.commit()


def read_doctor_category(session: sessionmaker):
    with session() as session:
        stmt = select(Category).order_by(Category.id)
        return session.scalars(stmt).all()


def create_service(session: sessionmaker, name, price):
    with session() as session:
        service = Service(
            name=name,
            price=price,
        )
        session.add(service)
        session.commit()


def read_service(session: sessionmaker):
    with session() as session:
        stmt = select(Service).order_by(Service.id)
        return session.scalars(stmt).all()


def update_service(session: sessionmaker, service_id, price=None, available=None):
    with session.begin() as conn:

        if price is not None and available is not None:
            stmt = update(Service).where(Service.id == service_id).values(price=price, available=available)

        elif price is not None:
            stmt = update(Service).where(Service.id == service_id).values(price=price)

        elif available is not None:
            stmt = update(Service).where(Service.id == service_id).values(available=available)

        else:
            raise ValueError

        conn.execute(stmt)


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


def create_visiting_session(session: sessionmaker, patient_id):
    with session() as session:
        visiting_session = VisitingSession(patient_id=patient_id)

        session.add(visiting_session)
        session.commit()


def read_visiting_session(session: sessionmaker):
    with session() as session:
        stmt = select(VisitingSession).order_by(VisitingSession.id)
        return session.scalars(stmt).all()


def read_visiting_session_by_patient_id(session: sessionmaker, patient_id):
    with session() as session:
        stmt = select(VisitingSession).where(VisitingSession.patient_id == patient_id).order_by(VisitingSession.id)
        return session.scalars(stmt).all()
