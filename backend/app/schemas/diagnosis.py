from pydantic import BaseModel


class Diagnosis(BaseModel):
    id: int
    name: str
