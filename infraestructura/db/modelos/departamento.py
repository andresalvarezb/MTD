from infraestructura.db.index import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .municipio import MunicipioORM


class DepartamentoORM(Base):
    __tablename__ = "departamento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)

    # Relaciones N:1
    municipios: Mapped[list["MunicipioORM"]] = relationship(back_populates="departamento")
