# from __future__ import annotations
from datetime import datetime
from infraestructura.db.index import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, Enum

# from core.models.enums import EstadoUsuarioEnum, ContratoUsuarioEnum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .municipio import MunicipioORM
    from .cargo import CargoORM
    from .historialLaboralUsuario import HistorialLaboralORM
    from .cuentaBancaria import CuentaBancariaORM
    from .descuento import DescuentosPorPagarORM
    from .deuda import DeudaORM


class UsuarioORM(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    estado: Mapped[str] = mapped_column(String(45), nullable=False)
    id_municipio: Mapped[int] = mapped_column(
        ForeignKey("municipio.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    contrato: Mapped[str] = mapped_column(String(45), nullable=False)
    id_cargo: Mapped[int] = mapped_column(
        ForeignKey("cargo.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    correo: Mapped[str | None] = mapped_column(String(45), nullable=True, unique=True)
    telefono: Mapped[str | None] = mapped_column(String(45), nullable=True)
    seguridad_social: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    fecha_aprobacion_seguridad_social: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_ultima_contratacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relaciones 1:N
    municipio: Mapped["MunicipioORM"] = relationship(back_populates="usuarios")
    historial_laboral: Mapped[list["HistorialLaboralORM"]] = relationship(back_populates="usuario")
    cargo: Mapped["CargoORM"] = relationship(back_populates="usuarios")
    cuentas_bancarias: Mapped[list["CuentaBancariaORM"]] = relationship(back_populates="usuario")
    descuentos: Mapped[list["DescuentosPorPagarORM"]] = relationship(back_populates="usuario")
    deudas: Mapped[list["DeudaORM"]] = relationship(back_populates="usuario")
