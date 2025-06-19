from core.entidades.cargo import Cargo
from core.interfaces.repositorioCargo import RepositorioCargo


class CrearCargo:
    def __init__(self, repositorio: RepositorioCargo):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Cargo:
        cargo = Cargo(nombre=datos["cargo"])
        cargo = self.repositorio.guardar(cargo)
        return cargo
