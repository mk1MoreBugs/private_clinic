from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from .users import create_user_and_flush
from .. import PatientCategory
from ..models.patient import Patient
from ..models.user import User


def create_patient(
        session: Session,
        last_name: str,
        first_name: str,
        birthday: date,
        hashed_password: str,
        middle_name: str | None = None,
        category_id: int | None = None,
):
    user = create_user_and_flush(
        session=session,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        hashed_password=hashed_password,
    )

    patient = Patient(
        user_id=user.id,
        birthday=birthday,
        category_id=category_id,
    )
    session.add(patient)
    session.commit()


def read_patients(session: Session):
    stmt = select(
        Patient.user_id.label("patient_id"),
        User.last_name,
        User.first_name,
        User.middle_name,
        Patient.birthday,
        PatientCategory.name.label("category_name"),
        PatientCategory.id.label("category_id")
    ).select_from(
        Patient,
    ).join(
        User
    ).join(
        PatientCategory, isouter=True,
    ).order_by(
        User.last_name,
    )

    return session.execute(stmt).mappings().all()  # return list[dict]


def read_patient_by_id(session: Session, user_id: int):
    stmt = select(
        Patient
    ).select_from(
        Patient,
    ).where(
        Patient.user_id == user_id
    )
    result = session.execute(stmt)

    return result.scalars().one_or_none()
