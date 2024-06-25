from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    experience: Mapped[int]
    quit_clinic: Mapped[bool] = mapped_column(default=False)  # Уволен ли
    speciality_id: Mapped[int] = mapped_column(ForeignKey("specialities.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    user: Mapped["User"] = relationship(back_populates="doctor")
    speciality: Mapped["DoctorSpeciality"] = relationship(back_populates="doctors")
    category: Mapped["DoctorCategory"] = relationship(back_populates="doctors")
    visits: Mapped[list["Visit"]] = relationship(back_populates="doctor")

    def __repr__(self) -> str:
        return (f"Doctor("
                f"user_id={self.user_id!r}, "
                f"experience={self.experience!r}, "
                f"quit_clinic={self.quit_clinic!r}, "
                f"speciality_id={self.speciality_id!r}, "
                f"category_id={self.category_id!r})"
                )
