from datetime import date

from app.schemas.full_name import FullName


class PatientBase(FullName):
    birthday: date
    category_id: int | None


class PatientIn(PatientBase):
    hashed_password: str


class PatientOut(PatientBase):
    patient_id: int
    category_name: str | None
