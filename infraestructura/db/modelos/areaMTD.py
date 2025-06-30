from infraestructura.db.index import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .deuda import DeudaORM


class AreaMTDORM(Base):
    __tablename__ = "area_mtd"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)

    deudas: Mapped[list["DeudaORM"]] = relationship(back_populates="area")
