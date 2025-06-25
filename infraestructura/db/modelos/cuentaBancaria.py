from datetime import datetime
from sqlalchemy import DateTime
from infraestructura.db.index import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import UsuarioORM
    from .banco import BancoORM
    from .cuentaPorPagar import CuentaPorPagarORM


class CuentaBancariaORM(Base):
    __tablename__ = "cuenta_bancaria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero_cuenta: Mapped[str] = mapped_column(String(45), nullable=False, unique=True, index=True)
    numero_certificado: Mapped[str | None] = mapped_column(String(45), nullable=True)
    estado: Mapped[str] = mapped_column(String(255), nullable=True)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True
    )
    id_banco: Mapped[int] = mapped_column(
        ForeignKey("banco.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False
    )
    tipo_de_cuenta: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha_actualizacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relaciones N:1
    usuario: Mapped["UsuarioORM"] = relationship(back_populates="cuentas_bancarias")
    banco: Mapped["BancoORM"] = relationship(back_populates="cuentas_bancarias")
    cuenta_por_pagar: Mapped[list["CuentaPorPagarORM"]] = relationship(back_populates="cuenta_bancaria")
