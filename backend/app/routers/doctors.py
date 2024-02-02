from datetime import datetime

from fastapi import APIRouter


router = APIRouter(
    prefix="/doctors"
)


@router.get("/{doctor_id}")
async def read_visit_by_id(doctor_id: int, date_before: datetime | None = None, date_after: datetime | None = None):
    # Todo
    return {"message": "Hello world"}
