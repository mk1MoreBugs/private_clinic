from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status


from app.security.password import verify_password
from database.crud.doctors import read_doctor_by_id
from database.crud.patients import read_patient_by_id
from database.crud.users import read_hashed_password


def authenticate_user(
        user_id: str,
        password: str,
        session: Session,
) -> bool:
    hashed_password = read_hashed_password(
        session=session,
        user_id=string_to_integer(user_id),
    )

    if hashed_password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password not defined",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_verify_user = verify_password(
        plain_password=password,
        hashed_password=hashed_password,
    )
    return is_verify_user


def define_user_role(
        user_id: str,
        session: Session,
) -> str:
    roles = ""
    doctor_id = read_doctor_by_id(session=session, user_id=string_to_integer(user_id))
    patient_id = read_patient_by_id(session=session, user_id=string_to_integer(user_id))

    if doctor_id is not None:
        roles += "doctor,"
    if patient_id is not None:
        roles += "patient,"

    return roles


def string_to_integer(string: str) -> int:
    try:
        integer = int(string)
    except TypeError:
        integer = 0  # TODO
    return integer
