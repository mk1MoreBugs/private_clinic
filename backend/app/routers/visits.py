from datetime import datetime

from fastapi import APIRouter

router = APIRouter(
    prefix="/visits"
)


@router.get("/{visit_id}")
async def read_visit_by_id(visit_id: int, date_before: datetime | None = None, date_after: datetime | None = None):
    return {"visit_id": visit_id}  # Todo
