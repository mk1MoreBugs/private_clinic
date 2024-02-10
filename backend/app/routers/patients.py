from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.dependencies import session_db
from app.schemas.patient import PatientIn, PatientOut
from app.schemas.visiting_session import VisitingSessionOut
from database.crud import patients
from database.crud import visiting_sessions

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/")
async def read_patients(
        session: Session = Depends(session_db),
) -> list[PatientOut]:
    list_patients: list[PatientOut] = patients.read_patients(session)

    return list_patients


@router.get("/{patient_id}")
async def read_visiting_sessions_by_patient_id(
        patient_id: int,
        session: Session = Depends(session_db),
) -> list[VisitingSessionOut]:
    list_sessions = visiting_sessions.read_visiting_session(
        session=session,
        patient_id=patient_id,
    )
    return list_sessions


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_patient(
        patient: PatientIn,
        session: Session = Depends(session_db),
):
    patients.create_patient(session=session, **dict(patient))
