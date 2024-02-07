from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    visits: Mapped[list["Visit"]] = relationship(back_populates="diagnosis")

    def __repr__(self) -> str:
        return (f"Diagnosis("
                f"id={self.id!r}, "
                f"name={self.name!r})"
                )
