from typing import Annotated

from pydantic import Field
from app.schemas.user import FullName


class BaseDoctor(FullName):
    experience: Annotated[int, Field(ge=0, le=100)]


class DoctorIn(BaseDoctor):
    hashed_password: str
    speciality_id: int
    category_id: int


class DoctorOut(BaseDoctor):
    quit_clinic: bool = False
    doctor_id: int | None
    speciality_name: str | None
    category_name: str | None
