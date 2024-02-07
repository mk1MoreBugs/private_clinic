import enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from .base import Base


class CategoryEnum(enum.StrEnum):
    second = "Вторая категория"
    first = "Первая категория"
    highest = "Высшая категория"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Enum(CategoryEnum))

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return (f"Category("
                f"id={self.id!r}, "
                f"name={self.name!r})"
                )
