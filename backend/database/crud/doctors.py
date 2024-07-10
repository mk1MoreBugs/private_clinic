from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import update

from database import Doctor, DoctorSpeciality, DoctorCategory
from database.crud.users import create_user_and_flush
from database.models.user import User


def create_doctor(
        session: Session,
        last_name: str,
        first_name: str,
        hashed_password: str,
        experience: int,
        speciality_id: int,
        category_id: int,
        middle_name: str | None = None,
):
    user = create_user_and_flush(
        session=session,
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        hashed_password=hashed_password,
    )

    doctor = Doctor(
        user_id=user.id,
        experience=experience,
        speciality_id=speciality_id,
        category_id=category_id,
    )
    session.add(doctor)
    session.commit()


def read_doctors(session: Session):
    stmt = select(
        Doctor.user_id.label("doctor_id"),
        User.last_name,
        User.first_name,
        User.middle_name,
        Doctor.experience,
        Doctor.quit_clinic,
        DoctorSpeciality.name.label("speciality_name"),
        DoctorCategory.name.label("category_name"),
    ).select_from(
        Doctor,
    ).join(
        User
    ).join(
        DoctorSpeciality, isouter=True,
    ).join(
        DoctorCategory, isouter=True,
    )

    return session.execute(stmt).mappings().all()  # return list[dict]


def read_doctor_by_id(session: Session, user_id: int):
    stmt = select(
        Doctor
    ).select_from(
        Doctor,
    ).where(
        Doctor.user_id == user_id
    )
    result = session.execute(stmt)

    return result.scalars().one_or_none()


def quit_doctor(
        session: Session,
        doctor_id: int,
):
    stmt = update(Doctor).where(Doctor.user_id == doctor_id).values(quit_clinic=True)

    session.execute(stmt)
    session.commit()
