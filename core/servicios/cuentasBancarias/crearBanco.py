from core.entidades.banco import Banco
from core.interfaces.repositorioBanco import RepositorioBanco


class CrearBanco:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Banco:
        banco = Banco(nombre=datos["banco"])

        banco = self.repositorio.guardar(banco)

        return banco
