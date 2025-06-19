from datetime import datetime
from infraestructura.db.index import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DECIMAL, ForeignKey, DATETIME


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioORM
    from .cuentaPorPagar import CuentaPorPagarORM
    from .deuda import DeudaORM




class DescuentosPorPagarORM(Base):
    __tablename__ = "descuentos_por_pagar"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_cuenta_por_pagar: Mapped[int] = mapped_column(ForeignKey("cuentas_por_pagar.id"), nullable=False, index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False, index=True)
    id_deuda: Mapped[int | None] = mapped_column(ForeignKey("deuda_usuario.id"), nullable=True, index=True)
    valor: Mapped[DECIMAL] = mapped_column(DECIMAL(18, 2), nullable=False, default=0.0)
    fecha_creacion: Mapped[datetime] = mapped_column(DATETIME, nullable=False, index=True)
    tipo_de_descuento: Mapped[str | None] = mapped_column(String(45), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(DATETIME, nullable=True)

    # Relaciones 1:N
    cuenta_por_pagar: Mapped["CuentaPorPagarORM"] = relationship(back_populates="descuentos")
    usuario: Mapped["UsuarioORM"] = relationship(back_populates="descuentos")
    deuda: Mapped["DeudaORM"] = relationship(back_populates="descuentos")

