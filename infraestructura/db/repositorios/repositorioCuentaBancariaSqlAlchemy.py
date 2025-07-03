from sqlalchemy.orm import Session
from datetime import datetime
from core.entidades.cuentaBancaria import CuentaBancaria
from infraestructura.db.modelos.cuentaBancaria import CuentaBancariaORM
from core.interfaces.repositorioCuentaBancaria import (
    CrearCuentaBancariaProtocol,
    ObtenerCuentaBancariaProtocol,
    ObtenerCuentaBancariaPorIdProtocol,
    ActualizarCuentaBancariaProtocol,
)


class RepositorioCuentaBancariaSqlAlchemy(
    ObtenerCuentaBancariaProtocol,
    CrearCuentaBancariaProtocol,
    ObtenerCuentaBancariaPorIdProtocol,
    ActualizarCuentaBancariaProtocol,
):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria:
        nueva_cuenta = CuentaBancariaORM(
            id_usuario=cuenta_bancaria.usuario.id,
            id_banco=cuenta_bancaria.banco.id,
            estado=cuenta_bancaria.estado,
            numero_cuenta=cuenta_bancaria.numero_cuenta,
            numero_certificado=cuenta_bancaria.numero_certificado,
            tipo_de_cuenta=cuenta_bancaria.tipo_de_cuenta,
            fecha_actualizacion=datetime.now(),
            observaciones=cuenta_bancaria.observaciones,
        )
        self.db.add(nueva_cuenta)
        self.db.flush()
        self.db.refresh(nueva_cuenta)
        return cuenta_bancaria.from_orm(nueva_cuenta)

    def obtener_por_numero(self, cuenta_bancaria: CuentaBancaria):
        registro_orm = self.db.query(CuentaBancariaORM).filter_by(numero_cuenta=cuenta_bancaria.numero_cuenta).first()
        if registro_orm:
            return CuentaBancaria.from_orm(registro_orm)
        else:
            return None

    def obtener_por_id(self, id_cuenta_bancaria: int):
        registro_orm = self.db.query(CuentaBancariaORM).filter_by(id=id_cuenta_bancaria).first()
        if registro_orm:
            return CuentaBancaria.from_orm(registro_orm)
        else:
            return None

    def actualizar(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria:
        registro_orm = self.db.query(CuentaBancariaORM).filter_by(numero_cuenta=cuenta_bancaria.numero_cuenta).first()
        if not registro_orm:
            raise ValueError("Cuenta bancaria no encontrada")

        if not cuenta_bancaria.usuario.id:
            raise ValueError("Usuario no asociado")

        if not cuenta_bancaria.banco.id:
            raise ValueError("Banco no asociado")

        registro_orm.numero_certificado = cuenta_bancaria.numero_certificado
        registro_orm.estado = cuenta_bancaria.estado
        registro_orm.id_usuario = cuenta_bancaria.usuario.id
        registro_orm.id_banco = cuenta_bancaria.banco.id
        registro_orm.tipo_de_cuenta = cuenta_bancaria.tipo_de_cuenta
        registro_orm.fecha_actualizacion = datetime.now()
        registro_orm.observaciones = cuenta_bancaria.observaciones

        self.db.flush()
        return CuentaBancaria.from_orm(registro_orm)
