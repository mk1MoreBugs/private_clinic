from datetime import datetime

from pydantic import BaseModel


class VisitingSessionOut(BaseModel):
    session_id: int
    date_start: datetime | None
    date_end: datetime | None
    sum_price: int | None
