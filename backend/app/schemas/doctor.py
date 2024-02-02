from pydantic import BaseModel

from app.schemas.full_name import FullName
from app.schemas.speciality import Speciality
from app.schemas.category import Category


class Doctor(BaseModel):
    full_name: FullName
    speciality: Speciality
    category: Category
    experience: int
