import enum
from typing import Annotated

from pydantic import BaseModel, Field


class FullName(BaseModel):
    last_name: Annotated[str, Field(max_length=50, examples=["Иванов"])]                  # Ф
    first_name: Annotated[str, Field(max_length=50, examples=["Иван"])]                 # И
    middle_name: Annotated[str | None, Field(max_length=50, examples=["Иванович"])] = None  # О


class User(BaseModel):
    user_id: int
    roles: str
