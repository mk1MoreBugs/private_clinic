from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import PatientCategory
from ..models.patient import Patient


def create_patient(
        session: Session,
        last_name: str,
        first_name: str,
        birthday: date,
        middle_name: str | None = None,
        category_id: int | None = None,
):
    patient = Patient(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        birthday=birthday,
        category_id=category_id,
    )
    session.add(patient)
    session.commit()


def read_patients(session: Session):
    stmt = select(
        Patient.id.label("patient_id"),
        Patient.last_name,
        Patient.first_name,
        Patient.middle_name,
        Patient.birthday,
        PatientCategory.name.label("category_name"),
        PatientCategory.id.label("category_id")
    ).select_from(
        Patient,
    ).join(
        PatientCategory, isouter=True,
    ).order_by(
        Patient.last_name,
    )

    return session.execute(stmt).mappings().all()  # return list[dict]
