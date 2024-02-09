from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


from ..models.doctor_category import Category


def create_doctor_category(session: sessionmaker, name):
    with session() as session:
        doctor_category = Category(name=name)
        session.add(doctor_category)
        session.commit()


def read_doctor_category(session: sessionmaker):
    with session() as session:
        stmt = select(Category).order_by(Category.id)
        return session.scalars(stmt).all()
