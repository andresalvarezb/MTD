from sqlalchemy.orm import Session
from core.entidades.cuentaBancaria import CuentaBancaria
from infraestructura.db.modelos.cuentaBancaria import CuentaBancariaORM
from core.interfaces.repositorioCuentaBancaria import RepositorioCuentaBancaria


class RepositorioCuentaBancariaSqlAlchemy(RepositorioCuentaBancaria):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria:
        """Implementación para guardar un CuentaBancaria en la base de datos"""

        # verificar existencia
        existe = self.obtener(cuenta_bancaria)
        if existe:
            cuenta_bancaria.id = existe.id
            return cuenta_bancaria

        # creacion
        nueva_cuenta_bancaria = CuentaBancariaORM(**cuenta_bancaria.__dict__)
        self.db.add(nueva_cuenta_bancaria)
        self.db.flush()
        self.db.refresh(nueva_cuenta_bancaria)

        cuenta_bancaria.id = nueva_cuenta_bancaria.id
        return cuenta_bancaria

    def obtener(self, cuenta_bancaria: CuentaBancaria):
        existe = self.db.query(CuentaBancariaORM).filter_by(numero_cuenta=cuenta_bancaria.numero_cuenta).first()
        if existe:
            return existe
        else:
            return None
