from infraestructura.db.index import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioORM
    from .historialLaboralUsuario import HistorialLaboralORM


class CargoORM(Base):
    __tablename__ = "cargo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, default="SIN CARGO", index=True)

    historial_laboral: Mapped[list["HistorialLaboralORM"]] = relationship(back_populates="cargo")
    usuarios: Mapped[list["UsuarioORM"]] = relationship(back_populates="cargo")
