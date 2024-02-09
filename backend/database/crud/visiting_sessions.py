from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from .. import Visit
from ..models.visiting_session import VisitingSession


def create_visiting_session(session: sessionmaker, patient_id):
    with session() as session:
        visiting_session = VisitingSession(patient_id=patient_id)

        session.add(visiting_session)
        session.commit()


def read_visiting_session(session: sessionmaker, patient_id):
    with session() as session:

        stmt = select(
            VisitingSession.id.label("session_id"),
            func.min(Visit.appointment_datetime).label("date_start"),
            func.max(Visit.appointment_datetime).label("date_end"),
            func.sum(Visit.discounted_price).label("sum_price"),
        ).join(
            VisitingSession
        ).where(
            VisitingSession.patient_id == patient_id,
        ).group_by(
            VisitingSession.id,
        ).order_by(
            func.sum(Visit.discounted_price).desc()
        )

        return session.execute(stmt).mappings().all()  # return list[dict]
