from datetime import datetime

from pydantic import BaseModel

from app.schemas.full_name import FullName


class Patient(BaseModel):
    full_name: FullName
    birthday: datetime
