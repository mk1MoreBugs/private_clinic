from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .doctor_category import Category
    from .doctor_speciality import Speciality
    from .visit import Visit
from .base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    experience: Mapped[int]
    quit: Mapped[bool] = mapped_column(default=False)  # Уволен ли
    speciality_id: Mapped[int] = mapped_column(ForeignKey("specialities.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    speciality: Mapped["Speciality"] = relationship(back_populates="doctors")
    category: Mapped["Category"] = relationship(back_populates="doctors")
    visits: Mapped[list["Visit"]] = relationship(back_populates="doctor")

    def __repr__(self) -> str:
        return (f"Doctor("
                f"id={self.id!r}, "
                f"last_name={self.last_name!r}, "
                f"first_name={self.first_name!r}, "
                f"middle_name={self.middle_name!r}, "
                f"experience={self.experience!r}, "
                f"quit={self.quit!r}, "
                f"speciality_id={self.speciality_id!r}, "
                f"category_id={self.category_id!r})"
                )
