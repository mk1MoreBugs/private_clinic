from typing import Annotated

from pydantic import BaseModel, Field


class FullName(BaseModel):
    last_name: Annotated[str, Field(max_length=50)]                  # Ф
    first_name: Annotated[str, Field(max_length=50)]                 # И
    middle_name: Annotated[str | None, Field(max_length=50)] = None  # О
