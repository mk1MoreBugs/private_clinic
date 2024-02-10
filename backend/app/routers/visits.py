from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Path

from app.dependencies import session_db
from app.schemas.patient import PatientIn
from app.schemas.visit import VisitById, UpdateVisit, VisitIn
from database.crud import patients
from database.crud import visits

router = APIRouter(
    prefix="/visits",
    tags=["visits"],
)


@router.get("/{visit_id}")
async def read_visit_by_visit_id(
        visit_id: Annotated[int, Path()],
        session: Session = Depends(session_db),
) -> list[VisitById]:
    visit_by_id = visits.read_visit_by_id(session, visit_id)
    return visit_by_id


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_visit(
        visit: VisitIn,
        session: Session = Depends(session_db),
):
    visits.create_visit(session=session, **dict(visit))


@router.put("/update/{visit_id}")
async def update_visit(
        visit_id: int,
        update_data: UpdateVisit,
        session: Session = Depends(session_db),
):
    visits.update_visit(session=session, visit_id=visit_id, **dict(update_data))


@router.delete("/delete/{visit_id}")
async def delete_visit(
        visit_id: int,
        session: Session = Depends(session_db),
):
    visits.delete_visit(session=session, visit_id=visit_id)
