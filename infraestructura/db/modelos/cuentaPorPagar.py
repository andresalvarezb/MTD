from datetime import datetime
from infraestructura.db.index import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DECIMAL, ForeignKey, DATETIME, BOOLEAN

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .historialLaboralUsuario import HistorialLaboralORM
    from .cuentaBancaria import CuentaBancariaORM
    from .descuento import DescuentosPorPagarORM


class CuentaPorPagarORM(Base):
    __tablename__ = "cuentas_por_pagar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_historial_laboral: Mapped[int] = mapped_column(
        ForeignKey("historial_laboral.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True
    )
    id_cuenta_bancaria: Mapped[int] = mapped_column(
        ForeignKey("cuenta_bancaria.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    claveCPP: Mapped[str] = mapped_column(String(45), nullable=False)
    fecha_prestacion_servicio: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    fecha_radicacion_contable: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    estado_de_pago: Mapped[str | None] = mapped_column(String(45), nullable=True)
    estado_aprobacion_cuenta_usuario: Mapped[str] = mapped_column(String(45), nullable=True)
    estado_cuenta_por_pagar: Mapped[str] = mapped_column(String(45), nullable=True)
    valor_cuenta_cobro: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False)
    total_descuentos: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False)
    total_a_pagar: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False)
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_aprobacion_rut: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_creacion: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_aprobacion_cuenta_usuario: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_programacion_pago: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_reprogramacion: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    fecha_pago: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)
    estado_reprogramacion_pago: Mapped[str | None] = mapped_column(String(45), nullable=True)
    rut: Mapped[bool] = mapped_column(BOOLEAN, nullable=False, default=False)
    dse: Mapped[str | None] = mapped_column(String(45), nullable=True)
    causal_rechazo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    creado_por: Mapped[str | None] = mapped_column(String(45), nullable=True)
    lider_paciente_asignado: Mapped[str | None] = mapped_column(String(45), nullable=True)
    eps_paciente_asignado: Mapped[str | None] = mapped_column(String(45), nullable=True)
    tipo_de_cuenta: Mapped[str | None] = mapped_column(String(45), nullable=True)

    # Relaciones 1:N
    historial_laboral: Mapped["HistorialLaboralORM"] = relationship(back_populates="cuentas_por_pagar")
    cuenta_bancaria: Mapped["CuentaBancariaORM"] = relationship(back_populates="cuenta_por_pagar")
    descuentos: Mapped[list["DescuentosPorPagarORM"]] = relationship(back_populates="cuenta_por_pagar")
