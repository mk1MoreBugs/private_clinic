from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.dependencies import session_db
from app.schemas.doctor import DoctorIn, DoctorOut
from app.schemas.visit import VisitSelectForDoctor
from database.crud import doctors
from database.crud import visits

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get("/")
async def read_doctors(session: Session = Depends(session_db)) -> list[DoctorOut]:
    list_doctors: list[DoctorOut] = doctors.read_doctors(session)

    return list_doctors


@router.get("/{doctor_id}")
async def read_visits_by_doctor_id(
        doctor_id: int,
        session: Session = Depends(session_db),
) -> list[VisitSelectForDoctor]:
    visits_by_doctor_id: list[VisitSelectForDoctor] = visits.read_visits_like_doctor(
        session=session,
        doctor_id=doctor_id,
    )
    return visits_by_doctor_id


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_doctor(
        doctor: DoctorIn,
        session: Session = Depends(session_db),
):
    doctors.create_doctor(session, **dict(doctor))
