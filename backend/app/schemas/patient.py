from datetime import date

from app.schemas.full_name import FullName


class PatientIn(FullName):
    birthday: date
    category_id: int | None


class PatientOut(PatientIn):
    patient_id: int
    category_name: str | None
