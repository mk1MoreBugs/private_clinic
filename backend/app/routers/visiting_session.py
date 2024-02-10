from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, Query, Body, status

from app.dependencies import session_db
from app.routers import visits
from app.schemas.visit import VisitSelectForPatient
from database.crud import visiting_sessions
from database.crud import visits

router = APIRouter(
    prefix="/session",
    tags=["visiting_session"],
)


@router.get("/{session_id}")
async def read_visits(
        session_id: Annotated[int, Path()],
        detailed: Annotated[bool, Query()] = False,
        session: Session = Depends(session_db),
) -> list[VisitSelectForPatient]:
    list_visits = visits.read_visits(
        session=session,
        visit_session_id=session_id,
        detailed_information=detailed,
    )
    return list_visits


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def read_visiting_session_by_patient_id(
        patient_id: Annotated[int, Body()],
        session: Session = Depends(session_db),
):
    visiting_sessions.create_visiting_session(session=session, patient_id=patient_id)

