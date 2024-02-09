from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from database import Doctor, DoctorSpeciality, DoctorCategory


def create_doctor(
        session: sessionmaker,
        last_name: str,
        first_name: str,
        middle_name: str,
        experience: int,
        speciality_id: int,
        category_id: int,
):
    with session() as session:
        doctor = Doctor(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            experience=experience,
            speciality_id=speciality_id,
            category_id=category_id,
        )
        session.add(doctor)
        session.commit()


def read_doctors(session: sessionmaker):
    with session() as session:
        stmt = select(
            Doctor.last_name,
            Doctor.first_name,
            Doctor.middle_name,
            Doctor.experience,
            Doctor.quit_clinic,
            DoctorSpeciality.name.label("speciality_name"),
            DoctorCategory.name.label("category_name"),
        ).select_from(
            Doctor,
        ).join(
            DoctorSpeciality, isouter=True,
        ).join(
            DoctorCategory, isouter=True,
        )

        return session.execute(stmt).mappings().all()  # return list[dict]


def quit_doctor(
        session: sessionmaker,
        doctor_id: int,
):
    stmt = update(Doctor).where(Doctor.id == doctor_id).values(quit_clinic=True)

    with session() as session:
        session.execute(stmt)
        session.commit()
