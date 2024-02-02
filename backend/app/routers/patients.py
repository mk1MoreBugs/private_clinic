from datetime import datetime

from fastapi import APIRouter


router = APIRouter(
    prefix="/patients"
)


@router.get("/{patient_id}")
async def read_visit_by_id(patient_id: int, date_before: datetime | None = None, date_after: datetime | None = None):
    # Todo
    return {"message": "Hello world"}

