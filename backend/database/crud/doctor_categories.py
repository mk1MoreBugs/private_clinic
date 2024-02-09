from sqlalchemy import select
from sqlalchemy.orm import Session


from ..models.doctor_category import DoctorCategory


def create_doctor_category(session: Session, name: str):
    doctor_category = DoctorCategory(name=name)
    session.add(doctor_category)
    session.commit()


def read_doctor_category(session: Session):
    stmt = select(DoctorCategory).order_by(DoctorCategory.id)
    return session.scalars(stmt).all()
