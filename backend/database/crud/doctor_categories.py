from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


from ..models.doctor_category import DoctorCategory


def create_doctor_category(session: sessionmaker, name):
    with session() as session:
        doctor_category = DoctorCategory(name=name)
        session.add(doctor_category)
        session.commit()


def read_doctor_category(session: sessionmaker):
    with session() as session:
        stmt = select(DoctorCategory).order_by(DoctorCategory.id)
        return session.scalars(stmt).all()
