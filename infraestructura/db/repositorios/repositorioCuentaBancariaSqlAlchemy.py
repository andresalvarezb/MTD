from sqlalchemy.orm import Session
from core.entidades.cuentaBancaria import CuentaBancaria
from infraestructura.db.modelos.cuentaBancaria import CuentaBancariaORM
from core.interfaces.repositorioCuentaBancaria import CrearCuentaBancariaProtocol,ObtenerCuentaBancariaProtocol, ObtenerCuentaBancariaPorIdProtocol


class RepositorioCuentaBancariaSqlAlchemy(ObtenerCuentaBancariaProtocol, CrearCuentaBancariaProtocol, ObtenerCuentaBancariaPorIdProtocol):
    def __init__(self, db: Session):
        self.db = db

    # def guardar(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria:
    #     """Implementación para guardar un CuentaBancaria en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(cuenta_bancaria)
    #     if existe:
    #         cuenta_bancaria.id = existe.id
    #         return cuenta_bancaria

    #     # creacion
    #     nueva_cuenta_bancaria = CuentaBancariaORM(**cuenta_bancaria.__dict__)
    #     self.db.add(nueva_cuenta_bancaria)
    #     self.db.flush()
    #     self.db.refresh(nueva_cuenta_bancaria)

    #     cuenta_bancaria.id = nueva_cuenta_bancaria.id
    #     return cuenta_bancaria

    def crear(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria:
        nueva_cuenta = CuentaBancariaORM(**cuenta_bancaria.__dict__)
        self.db.add(nueva_cuenta)
        self.db.flush()
        self.db.refresh(nueva_cuenta)
        cuenta_bancaria.id = nueva_cuenta.id
        return cuenta_bancaria

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