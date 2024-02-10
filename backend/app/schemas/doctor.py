from typing import Annotated

from pydantic import Field
from app.schemas.full_name import FullName


class BaseDoctor(FullName):
    experience: Annotated[int, Field(ge=0, le=100)]


class DoctorIn(BaseDoctor):
    speciality_id: int
    category_id: int


class DoctorOut(BaseDoctor):
    quit_clinic: bool | None
    doctor_id: int | None
    speciality_name: str | None
    category_name: str | None
