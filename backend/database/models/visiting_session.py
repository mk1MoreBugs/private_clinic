from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class VisitingSession(Base):
    __tablename__ = "visiting_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    patient_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("patients.user_id", onupdate="CASCADE", ondelete="SET NULL")
    )

    patient: Mapped["Patient"] = relationship(back_populates="visiting_sessions")

    def __repr__(self) -> str:
        return (f"VisitingSession("
                f"id={self.id!r}, "
                f"patient_id={self.patient_id!r})"
                )
