from fastapi import APIRouter, status

from app.dependencies import SessionDep, TokenDep
from app.schemas.doctor import DoctorIn, DoctorOut
from app.schemas.user import User
from app.schemas.visit import VisitSelectForDoctor
from app.security.access_token import get_token_data
from database.crud import doctors
from database.crud import visits

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get("/")
async def read_doctors(session: SessionDep, token: TokenDep) -> list[DoctorOut | None]:
    user = get_token_data(token)
    if verify_doctor(user):
        list_doctors: list[DoctorOut] = doctors.read_doctors(session)
        return list_doctors
    else:
        return []


@router.get("/{doctor_id}")
async def read_visits_by_doctor_id(
        doctor_id: int,
        session: SessionDep,
        token: TokenDep,
) -> list[VisitSelectForDoctor | None]:
    user = get_token_data(token)
    if verify_doctor(user):
        visits_by_doctor_id: list[VisitSelectForDoctor] = visits.read_visits_like_doctor(
            session=session,
            doctor_id=doctor_id,
        )
        return visits_by_doctor_id
    else:
        return []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_doctor(
        doctor: DoctorIn,
        session: SessionDep,
        token: TokenDep,
):
    user = get_token_data(token)
    if verify_doctor(user):
        doctors.create_doctor(session, **dict(doctor))


def verify_doctor(user: User):
    if "doctor" in user.roles:
        return True
    else:
        return False
