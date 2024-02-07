from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)

    visiting_session_id: Mapped[int] = mapped_column(
        ForeignKey("visiting_sessions.id", onupdate="CASCADE", ondelete="SET NULL")
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    diagnosis_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("diagnoses.id", onupdate="CASCADE", ondelete="RESTRICT")
    )
    appointment_datetime: Mapped[datetime]
    discounted_price: Mapped[int]
    anamnesis: Mapped[Optional[str]]
    opinion: Mapped[Optional[str]]

    doctor: Mapped["Doctor"] = relationship(back_populates="visits")
    service: Mapped["Service"] = relationship(back_populates="visits")
    diagnosis: Mapped["Diagnosis"] = relationship(back_populates="visits")

    def __repr__(self) -> str:
        return (f"Visit("
                f"id={self.id!r}, "
                f"visiting_session_id={self.visiting_session_id!r}, "
                f"doctor_id={self.doctor_id!r}, "
                f"service_id={self.service_id!r}, "
                f"diagnosis_id={self.diagnosis_id!r}, "
                f"appointment_datetime={self.appointment_datetime!r}, "
                f"discounted_price={self.discounted_price!r}, "
                f"anamnesis={self.anamnesis!r}, "
                f"opinion={self.opinion!r})"
                )
