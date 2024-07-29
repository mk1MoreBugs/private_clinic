from fastapi import APIRouter, status

from app.dependencies import SessionDep, TokenDep
from app.routers.doctors import verify_doctor
from app.schemas.patient import PatientIn, PatientOut
from app.schemas.user import User
from app.schemas.visiting_session import VisitingSessionOut
from app.security.access_token import get_token_data
from app.security.password import get_password_hash
from database.crud import patients
from database.crud import visiting_sessions

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get("/")
async def read_patients(
        session: SessionDep,
        token: TokenDep,
) -> list[PatientOut | None]:
    user = get_token_data(token)
    if verify_doctor(user):
        list_patients: list[PatientOut] = patients.read_patients(session)
        return list_patients
    else:
        print("Access is denied!")
        return []


@router.get("/{patient_id}")
async def read_visiting_sessions_by_patient_id(
        patient_id: int,
        session: SessionDep,
        token: TokenDep,
) -> list[VisitingSessionOut | None]:
    user = get_token_data(token)
    if __verify_patient(user):
        list_sessions = visiting_sessions.read_visiting_session(
            session=session,
            patient_id=patient_id,
        )
        return list_sessions
    else:
        return []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_patient(
        patient: PatientIn,
        session: SessionDep,
):
    hashed_password = get_password_hash(patient.plain_password)

    patients.create_patient(
        session=session,
        last_name=patient.last_name,
        first_name=patient.first_name,
        middle_name=patient.middle_name,
        birthday=patient.birthday,
        category_id=patient.category_id,
        hashed_password=hashed_password,
    )


def __verify_patient(user: User):
    if "patient" in user.roles:
        return True
    else:
        return False
