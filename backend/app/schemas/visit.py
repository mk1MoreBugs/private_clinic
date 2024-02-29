from datetime import datetime, date
from typing import Annotated

from pydantic import BaseModel, Field


class BaseVisit(BaseModel):
    appointment_datetime: datetime
    discounted_price: int


class VisitIn(BaseVisit):
    visiting_session_id: int
    service_id: int
    doctor_id: int
    diagnosis_id: int | None = None
    anamnesis: Annotated[str | None, Field(max_length=1000)] = None
    opinion: Annotated[str | None, Field(max_length=1000)] = None


class VisitBaseSelect(BaseVisit):
    visit_id: int
    service_name: str
    discount_percentage: Annotated[int, Field(ge=0, le=100)] | None


class VisitSelectForDoctor(VisitBaseSelect):
    patient_last_name: str
    patient_first_name: str
    patient_middle_name: str | None = None


class VisitSelectForPatient(VisitBaseSelect):
    doctor_last_name: Annotated[str, Field(max_length=50)]
    doctor_first_name: Annotated[str, Field(max_length=50)]
    doctor_middle_name: Annotated[str | None, Field(max_length=50)] = None
    category_name: str
    speciality_name: str


class VisitById(VisitSelectForDoctor, VisitSelectForPatient):
    patient_birthday: date
    diagnosis_name: str | None
    anamnesis: str | None
    opinion: str | None
    doctor_experience: int


class UpdateVisit(BaseModel):
    appointment_datetime: datetime | None = None
    diagnosis_id: int | None = None
    anamnesis: str | None = None
    opinion: str | None = None
