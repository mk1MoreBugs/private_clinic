from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .visit import Visit
from .base import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
    available: Mapped[bool] = mapped_column(default=True)

    visits: Mapped[list["Visit"]] = relationship(back_populates="service")

    def __repr__(self) -> str:
        return (f"Service("
                f"id={self.id!r}, "
                f"name={self.name!r}, "
                f"price={self.price!r}, "
                f"available={self.available!r})"
                )
