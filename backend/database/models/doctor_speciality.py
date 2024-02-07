from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Speciality(Base):
    __tablename__ = "specialities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="speciality")

    def __repr__(self) -> str:
        return (f"Speciality("
                f"id={self.id!r}, "
                f"name={self.name!r})"
                )
