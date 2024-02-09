from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.doctor_speciality import DoctorSpeciality


def create_doctor_speciality(session: Session, name: str):
    doctor_speciality = DoctorSpeciality(
        name=name,
    )
    session.add(doctor_speciality)
    session.commit()


def read_doctor_speciality(session: Session):
    stmt = select(DoctorSpeciality).order_by(DoctorSpeciality.id)
    return session.scalars(stmt).all()
