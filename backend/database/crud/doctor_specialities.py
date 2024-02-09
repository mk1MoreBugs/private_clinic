from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from ..models.doctor_speciality import DoctorSpeciality


def create_doctor_speciality(session: sessionmaker, name):
    with session() as session:
        doctor_speciality = DoctorSpeciality(
            name=name,
        )
        session.add(doctor_speciality)
        session.commit()


def read_doctor_speciality(session: sessionmaker):
    with session() as session:
        stmt = select(DoctorSpeciality).order_by(DoctorSpeciality.id)
        return session.scalars(stmt).all()
