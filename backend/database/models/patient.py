from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Patient(Base):
    __tablename__ = "patients"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    birthday: Mapped[date]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("patient_categories.id"))

    user: Mapped["User"] = relationship(back_populates="patient")
    visiting_sessions: Mapped[list["VisitingSession"]] = relationship(back_populates="patient")
    category: Mapped["PatientCategory"] = relationship(back_populates="patients")

    def __repr__(self) -> str:
        return (f"Patient("
                f"user_id={self.user_id!r}, "
                f"birthday={self.birthday!r}, "
                f"category_id={self.category_id!r})"
                )
