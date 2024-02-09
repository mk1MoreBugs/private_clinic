from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import delete

from database import Visit, Doctor, Speciality, Category, Diagnosis, Service, Patient, PatientCategory, VisitingSession


def create_visit(
        session: sessionmaker,
        visiting_session_id: int,
        service_id: int,
        doctor_id: int,
        appointment_datetime: datetime,
        discounted_price: int,
        diagnosis_id: int | None = None,
        anamnesis: str | None = None,
        opinion: str | None = None,
):
    visit = Visit(
        visiting_session_id=visiting_session_id,
        service_id=service_id,
        doctor_id=doctor_id,
        appointment_datetime=appointment_datetime,
        discounted_price=discounted_price,
        diagnosis_id=diagnosis_id,
        anamnesis=anamnesis,
        opinion=opinion,
    )

    with session() as session:
        session.add(visit)
        session.commit()


def read_visits(
        session: sessionmaker,
        detailed_information: bool = False,
        visit_session_id: int | None = None,
        doctor_id: int | None = None,
        doctor_quit_clinic: bool = False,
):
    select_statement = [
        Visit.id.label("visit_id"),
        Visit.appointment_datetime,
        Visit.discounted_price,
        Service.name.label("service_name"),

    ]

    if doctor_id is None and visit_session_id is None:
        select_statement.extend(
            (
                Doctor.last_name.label("doctor_last_name"),
                Doctor.first_name.label("doctor_first_name"),
                Doctor.middle_name.label("doctor_middle_name"),
                Category.name.label("category_name"),
                Speciality.name.label("speciality_name"),
                Patient.last_name.label("patient_last_name"),
                Patient.first_name.label("patient_first_name"),
                Patient.middle_name.label("patient_middle_name"),
                Category.name.label("category_name"),
                Speciality.name.label("speciality_name"),
            )
        )

        where_statement = Doctor.quit_clinic == doctor_quit_clinic,

    elif doctor_id is not None:
        select_statement.extend(
            (
                Patient.last_name.label("patient_last_name"),
                Patient.first_name.label("patient_first_name"),
                Patient.middle_name.label("patient_middle_name"),
            )
        )
        where_statement = (
            Doctor.id == doctor_id,
        )
    else:
        select_statement.extend(
            (
                Doctor.last_name.label("doctor_last_name"),
                Doctor.first_name.label("doctor_first_name"),
                Doctor.middle_name.label("doctor_middle_name"),
                Category.name.label("category_name"),
                Speciality.name.label("speciality_name"),
            )
        )
        where_statement = (
            and_(
                VisitingSession.id == visit_session_id,
                Doctor.quit_clinic == doctor_quit_clinic,
            )
        )
    if detailed_information:
        select_statement.extend(
            (
                Diagnosis.name.label("diagnosis_name"),
                Visit.anamnesis,
                Visit.opinion,
            )
        )

    stmt = select(
        *select_statement
    ).select_from(
        Visit
    ).where(
        *where_statement
    ).join(
        Diagnosis, Diagnosis.id == Visit.diagnosis_id, isouter=True
    ).join(
        Service, Service.id == Visit.service_id
    ).join(
        VisitingSession, VisitingSession.id == Visit.visiting_session_id  # todo patient_id not None
    ).join(
        Patient, Patient.id == VisitingSession.patient_id  # todo doctor_id not None
    ).join(
        Doctor, Doctor.id == Visit.doctor_id  # todo patient_id not None
    ).join(
        Speciality, Speciality.id == Doctor.speciality_id # todo patient_id not None
    ).join(
        Category, Category.id == Doctor.category_id  # todo patient_id not None
    ).order_by(
        Visit.appointment_datetime
    )

    with session() as session:
        return session.execute(stmt).mappings().all()  # todo return list[dict]


def read_visit_by_id(
        session: sessionmaker,
        visit_id: int,
):
    stmt = select(
        Visit.id.label("visit_id"),
        Visit.appointment_datetime,
        Service.name.label("service_name"),

        Patient.last_name.label("patient_last_name"),
        Patient.first_name.label("patient_first_name"),
        Patient.middle_name.label("patient_middle_name"),
        Patient.birthday.label("patient_birthday"),

        Doctor.last_name.label("doctor_last_name"),
        Doctor.first_name.label("doctor_first_name"),
        Doctor.middle_name.label("doctor_middle_name"),
        Category.name.label("category_name"),
        Speciality.name.label("speciality_name"),

        Diagnosis.name.label("diagnosis_name"),
        Visit.anamnesis,
        Visit.opinion,
    ).select_from(
        Visit
    ).where(
        Visit.id == visit_id
    ).join(
        Diagnosis, Diagnosis.id == Visit.diagnosis_id, isouter=True
    ).join(
        Service, Service.id == Visit.service_id
    ).join(
        VisitingSession, VisitingSession.id == Visit.visiting_session_id  # todo patient_id not None
    ).join(
        Patient, Patient.id == VisitingSession.patient_id  # todo doctor_id not None
    ).join(
        Doctor, Doctor.id == Visit.doctor_id  # todo patient_id not None
    ).join(
        Speciality, Speciality.id == Doctor.speciality_id  # todo patient_id not None
    ).join(
        Category, Category.id == Doctor.category_id  # todo patient_id not None
    ).order_by(
        Visit.appointment_datetime
    )

    with session() as session:
        return session.execute(stmt).mappings().all()  # todo return list[dict]


def update_visit(
        session: sessionmaker,
        visit_id: int,
        appointment_datetime: datetime | None = None,
        diagnosis_id: int | None = None,
        anamnesis: str | None = None,
        opinion: str | None = None,
):
    with session() as session:
        if diagnosis_id is not None:
            stmt = update(Visit).where(Visit.id == visit_id).values(diagnosis_id=diagnosis_id)
            session.execute(stmt)

        if anamnesis is not None:
            stmt = update(Visit).where(Visit.id == visit_id).values(anamnesis=anamnesis)
            session.execute(stmt)

        if opinion is not None:
            stmt = update(Visit).where(Visit.id == visit_id).values(opinion=opinion)
            session.execute(stmt)

        if appointment_datetime is not None:
            stmt = update(Visit).where(Visit.id == visit_id).values(appointment_datetime=appointment_datetime)
            session.execute(stmt)

        session.commit()


def delete_visit(
    session: sessionmaker,
    visit_id: int,
):
    stmt = delete(Visit).where(Visit.id == visit_id)
    with session() as session:
        session.execute(stmt)
        session.commit()
