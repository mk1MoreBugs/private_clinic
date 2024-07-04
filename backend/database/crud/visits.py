import selectors
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy import delete

from database import Visit, Doctor, DoctorSpeciality, DoctorCategory, Diagnosis, Service, Patient, PatientCategory, \
    VisitingSession
from database.models.user import User


def create_visit(
        session: Session,
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

    session.add(visit)
    session.commit()


def read_visits_like_doctor(
        session: Session,
        doctor_id: int,
        detailed_information: bool = False,
):
    stmt = _select_visits_by_doctor_id(doctor_id, detailed_information)

    return session.execute(stmt).mappings().all()  # return list[dict]


def read_visits_like_patient(
        session: Session,
        patient_id: int,
        detailed_information: bool = False,
):
    stmt = _select_visits_by_patient_id(patient_id, detailed_information)

    return session.execute(stmt.select()).mappings().all()  # return list[dict]


def read_visits_by_visit_session_id(
        session: Session,
        visit_session_id: int,
        detailed_information: bool = False,
):
    statement_for_patient_id = select(
        VisitingSession.patient_id
    ).select_from(
        VisitingSession
    ).where(
        VisitingSession.id == visit_session_id
    )
    patient_id = session.execute(statement_for_patient_id).scalars().one()

    sub_select_for_user = _select_visits_by_patient_id(
        patient_id=patient_id,
        detailed_information=detailed_information,
    )

    stmt = select(
        sub_select_for_user,
        User.last_name.label("doctor_last_name"),
        User.first_name.label("doctor_first_name"),
        User.middle_name.label("doctor_middle_name"),
        DoctorCategory.name.label("category_name"),
        DoctorSpeciality.name.label("speciality_name"),
    ).select_from(
        sub_select_for_user,
    ).join(
        Visit, sub_select_for_user.c.visit_id == Visit.id,
    ).join(
        Doctor, Visit.doctor_id == Doctor.user_id
    ).join(
        DoctorSpeciality, Doctor.speciality_id == DoctorSpeciality.id
    ).join(
        DoctorCategory, Doctor.category_id == DoctorCategory.id
    ).join(
        User, Doctor.user_id == User.id
    ).order_by(
        Visit.appointment_datetime
    )

    return session.execute(stmt).mappings().all()  # return list[dict]


def read_visit_by_id(
        session: Session,
        visit_id: int,
):
    base_query = _base_select_visits(detailed_information=True)

    stmt = select(
        base_query,
        PatientCategory.discount_percentage,

        User.last_name.label("patient_last_name"),
        User.first_name.label("patient_first_name"),
        User.middle_name.label("patient_middle_name"),
        Patient.birthday.label("patient_birthday"),

        User.last_name.label("doctor_last_name"),
        User.first_name.label("doctor_first_name"),
        User.middle_name.label("doctor_middle_name"),
        Doctor.experience.label("doctor_experience"),
        DoctorCategory.name.label("category_name"),
        DoctorSpeciality.name.label("speciality_name"),

    ).select_from(
        base_query
    ).where(
        Visit.id == visit_id
    ).join(
        Visit, Visit.id == base_query.c.visit_id
    ).join(
        User, User.id == Patient.user_id
    ).join(
        VisitingSession, VisitingSession.id == Visit.visiting_session_id  # todo patient_id not None
    ).join(
        Patient, Patient.user_id == VisitingSession.patient_id  # todo doctor_id not None
    ).join(
        PatientCategory, PatientCategory.id == Patient.category_id, isouter=True
    ).join(
        Doctor, Doctor.user_id == Visit.doctor_id  # todo patient_id not None
    ).join(
        DoctorSpeciality, DoctorSpeciality.id == Doctor.speciality_id  # todo patient_id not None
    ).join(
        DoctorCategory, DoctorCategory.id == Doctor.category_id  # todo patient_id not None
    ).order_by(
        Visit.appointment_datetime
    )

    return session.execute(stmt).mappings().all()  # todo return list[dict]


def update_visit(
        session: Session,
        visit_id: int,
        appointment_datetime: datetime | None = None,
        diagnosis_id: int | None = None,
        anamnesis: str | None = None,
        opinion: str | None = None,
):
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
        session: Session,
        visit_id: int,
):
    stmt = delete(Visit).where(Visit.id == visit_id)

    session.execute(stmt)
    session.commit()


def _expand_list_with_detailed_information(expand_list: list):
    expand_list.extend(
            (
                Diagnosis.name.label("diagnosis_name"),
                Visit.anamnesis,
                Visit.opinion,
            )
        )
    return expand_list


def _base_select_visits(
        detailed_information: bool,
):
    select_statement = [
        Visit.id.label("visit_id"),
        Visit.appointment_datetime,
        Visit.discounted_price,
        Service.name.label("service_name"),
    ]

    if detailed_information:
        select_statement = _expand_list_with_detailed_information(select_statement)

    base_query = select(
        *select_statement
    ).select_from(
        Visit
    ).join(
        Diagnosis, Visit.diagnosis_id == Diagnosis.id, isouter=True
    ).join(
        Service, Visit.service_id == Service.id
    ).subquery()
    return base_query


def _select_visits_by_patient_id(
        patient_id: int,
        detailed_information: bool,
):
    base_query = _base_select_visits(detailed_information)

    stmt = select(
        base_query,
        PatientCategory.discount_percentage,

        Visit.visiting_session_id,
        User.last_name.label("doctor_last_name"),
        User.first_name.label("doctor_first_name"),
        User.middle_name.label("doctor_middle_name"),
        DoctorCategory.name.label("category_name"),
        DoctorSpeciality.name.label("speciality_name"),
    ).select_from(
        base_query
    ).where(
        Patient.user_id == patient_id,
    ).join(
        Visit, Visit.id == base_query.c.visit_id
    ).join(
        VisitingSession, Visit.visiting_session_id == VisitingSession.id
    ).join(
        Patient, VisitingSession.patient_id == Patient.user_id,
    ).join(
        PatientCategory, Patient.category_id == PatientCategory.id, isouter=True
    ).join(
        Doctor, Visit.doctor_id == Doctor.user_id
    ).join(
        DoctorSpeciality, Doctor.speciality_id == DoctorSpeciality.id
    ).join(
        DoctorCategory, Doctor.category_id == DoctorCategory.id
    ).join(
        User, Doctor.user_id == User.id
    ).order_by(
        Visit.appointment_datetime
    ).subquery()
    return stmt


def _select_visits_by_doctor_id(
        doctor_id: int,
        detailed_information: bool,
):
    base_query = _base_select_visits(detailed_information)

    stmt = select(
        base_query,
        PatientCategory.discount_percentage,

        User.last_name.label("patient_last_name"),
        User.first_name.label("patient_first_name"),
        User.middle_name.label("patient_middle_name"),

    ).select_from(
        base_query
    ).where(
        Doctor.user_id == doctor_id,
    ).join(
        Visit, Visit.id == base_query.c.visit_id
    ).join(
        VisitingSession, Visit.visiting_session_id == VisitingSession.id
    ).join(
        Patient, VisitingSession.patient_id == Patient.user_id,
    ).join(
        PatientCategory, Patient.category_id == PatientCategory.id, isouter=True
    ).join(
        User, Patient.user_id == User.id
    ).join(
        Doctor, Visit.doctor_id == Doctor.user_id
    ).order_by(
        Visit.appointment_datetime
    )
    return stmt
