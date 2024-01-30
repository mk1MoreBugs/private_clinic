from app.schemas.full_name import FullName


class Patient(FullName):
    patient_id: int
    birthday: str
