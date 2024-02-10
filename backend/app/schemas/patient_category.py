from typing import Annotated

from pydantic import Field
from app.schemas.base_item import BaseItem


class PatientCategory(BaseItem):
    discount_percentage: Annotated[int, Field(ge=0, le=100)]
    