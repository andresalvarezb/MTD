from datetime import datetime
from infraestructura.db.index import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DECIMAL, ForeignKey, DATETIME

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioORM
    from .descuento import DescuentosPorPagarORM
    from .areaMTD import AreaMTDORM


class DeudaORM(Base):
    __tablename__ = "deuda_usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(45), nullable=False)
    saldo: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False, default=0.0)
    valor_total: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False, default=0.0)
    fecha_creacion: Mapped[datetime] = mapped_column(DATETIME, nullable=False, index=True)
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    id_area: Mapped[int | None] = mapped_column(ForeignKey("area_mtd.id"), nullable=True, index=True)  # ! FALTA CREAR

    # Relaciones 1:N
    usuario: Mapped["UsuarioORM"] = relationship(back_populates="deudas")
    descuentos: Mapped[list["DescuentosPorPagarORM"]] = relationship(back_populates="deuda")
    area: Mapped["AreaMTDORM"] = relationship(back_populates="deudas")