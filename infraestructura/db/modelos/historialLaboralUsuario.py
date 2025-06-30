from datetime import datetime
from infraestructura.db.index import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cargo import CargoORM
    from .usuario import UsuarioORM
    from .municipio import MunicipioORM
    from .cuentaPorPagar import CuentaPorPagarORM


class HistorialLaboralORM(Base):
    __tablename__ = "historial_laboral"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_municipio: Mapped[int] = mapped_column(
        ForeignKey("municipio.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    contrato: Mapped[str] = mapped_column(String(45), nullable=False)
    id_cargo: Mapped[int] = mapped_column(
        ForeignKey("cargo.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    fecha_contratacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    claveHLU: Mapped[str] = mapped_column(String(45), nullable=False)
    seguridad_social: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)
    fecha_aprobacion_seguridad_social: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_ultima_contratacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_fin_contratacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True
    )

    # Relaciones 1:N
    usuario: Mapped["UsuarioORM"] = relationship(back_populates="historial_laboral")
    cargo: Mapped["CargoORM"] = relationship(back_populates="historial_laboral")
    cuentas_por_pagar: Mapped[list["CuentaPorPagarORM"]] = relationship(back_populates="historial_laboral")
    municipio: Mapped["MunicipioORM"] = relationship(back_populates="historial_laboral")
