from infraestructura.db.index import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioORM


class DepartamentoORM(Base):
    __tablename__ = "departamento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)

    # Relaciones N:1
    municipios: Mapped[list["MunicipioORM"]] = relationship(back_populates="departamento")


class MunicipioORM(Base):
    __tablename__ = "municipio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)

    id_departamento: Mapped[int] = mapped_column(
        ForeignKey("departamento.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )

    # Relaciones 1:N
    departamento: Mapped["DepartamentoORM"] = relationship(back_populates="municipios")
    usuarios: Mapped[list["UsuarioORM"]] = relationship(back_populates="municipio")
