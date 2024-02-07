from datetime import date
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    birthday: Mapped[date]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("patient_categories.id"))

    category: Mapped["PatientCategory"] = relationship("PatientCategory", back_populates="patients")
    visiting_sessions: Mapped[list["VisitingSession"]] = relationship(back_populates="patient")

    def __repr__(self) -> str:
        return (f"Patient("
                f"id={self.id!r}, "
                f"last_name={self.last_name!r}, "
                f"first_name={self.first_name!r}, "
                f"middle_name={self.middle_name!r}, "
                f"birthday={self.birthday!r}, "
                f"category_id={self.category_id!r})"
                )
