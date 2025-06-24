from core.entidades.municipio import Municipio, Departamento
from core.interfaces.repositorioMunicipio import RepositorioMunicipio, RepositorioDepartamento


class CrearDepartamento:
    def __init__(self, repositorio: RepositorioDepartamento):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Departamento:
        departamento = Departamento(nombre=datos["departamento"])
        departamento = self.repositorio.guardar(departamento)

        return departamento


class CrearMunicipio:
    def __init__(self, repositorio: RepositorioMunicipio):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Municipio:
        municipio = Municipio(nombre=datos["municipio"], id_departamento=datos["id_departamento"])
        municipio = self.repositorio.guardar(municipio)

        return municipio
