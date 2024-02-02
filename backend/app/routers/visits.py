from fastapi import APIRouter

from app.schemas.visits import Visits

router = APIRouter(
    prefix="/visits"
)


@router.get("/{visit_id}")
async def read_visit_by_id(visit_id: int):
    # Todo
    return Visits
