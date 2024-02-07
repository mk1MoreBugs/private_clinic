from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class PatientCategory(Base):
    __tablename__ = "patient_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    discount_percentage: Mapped[int]

    patients: Mapped[list["Patient"]] = relationship("Patient", back_populates="category")

    def __repr__(self) -> str:
        return (f"PatientCategory("
                f"id={self.id!r}, "
                f"category={self.category!r}, "
                f"discount_percentage={self.discount_percentage!r})"
                )
