from fastapi import APIRouter, status

from app.dependencies import SessionDep, TokenDep
from app.schemas.doctor import DoctorIn, DoctorOut, DoctorOutShort
from app.schemas.user import User, FullName
from app.schemas.visit import VisitSelectForDoctor
from app.security.access_token import get_token_data
from app.security.password import get_password_hash
from database.crud import doctors
from database.crud import visits

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get("/")
async def read_doctors(session: SessionDep, token: TokenDep) -> list[DoctorOut | DoctorOutShort | None]:
    user = get_token_data(token)
    if user is not None:
        list_doctors: list[DoctorOut] = doctors.read_doctors(session)
        if "doctor" in user.roles:
            return list_doctors
        elif "patient" in user.roles:
            return list(map(lambda item: DoctorOutShort(**dict(item)), list_doctors))
        else:
            return []
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
        hashed_password = get_password_hash(doctor.plain_password)

        doctors.create_doctor(
            session,
            last_name=doctor.last_name,
            first_name=doctor.first_name,
            middle_name=doctor.middle_name,
            hashed_password=hashed_password,
            experience=doctor.experience,
            speciality_id=doctor.speciality_id,
            category_id=doctor.category_id,


        )


def verify_doctor(user: User):
    if "doctor" in user.roles:
        return True
    else:
        return False
