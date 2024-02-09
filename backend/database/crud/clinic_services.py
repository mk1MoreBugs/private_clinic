from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from ..models.service import Service


def create_clinic_service(session: sessionmaker, name, price):
    with session() as session:
        service = Service(
            name=name,
            price=price,
        )
        session.add(service)
        session.commit()


def read_clinic_services(session: sessionmaker):
    with session() as session:
        stmt = select(Service).order_by(Service.id)
        return session.scalars(stmt).all()


def update_clinic_service(session: sessionmaker, service_id, price=None, available=None):
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
