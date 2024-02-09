from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import update

from ..models.service import Service


def create_clinic_service(session: Session, name: str, price: int):
    service = Service(
        name=name,
        price=price,
    )
    session.add(service)
    session.commit()


def read_clinic_services(session: Session):
    stmt = select(Service).order_by(Service.id)
    return session.scalars(stmt).all()


def update_clinic_service(session: Session, service_id: int, price: int = None, available: bool = True):
    if price is not None and available is False:
        stmt = update(Service).where(Service.id == service_id).values(price=price, available=available)

    elif price is not None:
        stmt = update(Service).where(Service.id == service_id).values(price=price)

    elif available is False:
        stmt = update(Service).where(Service.id == service_id).values(available=available)

    else:
        raise ValueError

    session.execute(stmt)
