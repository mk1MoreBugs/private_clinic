from datetime import datetime

from pydantic import BaseModel


class VisitingSessionOut(BaseModel):
    session_id: int
    date_start: datetime
    date_end: datetime
    sum_price: int
