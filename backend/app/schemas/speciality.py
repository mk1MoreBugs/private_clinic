from pydantic import BaseModel


class Speciality(BaseModel):
    id: int
    name: str
