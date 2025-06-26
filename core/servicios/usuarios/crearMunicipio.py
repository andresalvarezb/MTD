from core.entidades.municipio import Municipio, Departamento
from core.interfaces.repositorioMunicipio import (
    CrearMunicipioProtocol,
    ObtenerMunicipioPorNombreProtocol,
    ObtenerDepartamentoPorNombreProtocol,
    CrearDepartamentoProtocol,
)
from core.servicios.usuarios.dtos import CrearDepartamentoDTO, CrearMunicipioDTO


class CrearDepartamento:
    def __init__(self, repo_obtener: ObtenerDepartamentoPorNombreProtocol, repo_crear: CrearDepartamentoProtocol):
        self.repo_obtener = repo_obtener
        self.repo_crear = repo_crear

    def ejecutar(self, datos: CrearDepartamentoDTO) -> Departamento:
        # buscar departamento por nombre
        departamento = Departamento(nombre=datos.nombre)

        existe_departamento = self.repo_obtener.obtener_por_nombre(departamento)
        if existe_departamento:
            return existe_departamento

        # crearlo de no existir
        nuevo_departamento = self.repo_crear.crear(departamento)
        print(nuevo_departamento)
        return nuevo_departamento


class CrearMunicipio:
    def __init__(self, repo_crear: CrearMunicipioProtocol, repo_obtener: ObtenerMunicipioPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearMunicipioDTO) -> Municipio:
        # buscar municipio por nombre
        municipio = Municipio(nombre=datos.nombre, id_departamento=datos.id_departamento)

        existe_municipio = self.repo_obtener.obtener_por_nombre(municipio)
        if existe_municipio:
            return existe_municipio

        # crearlo de no existir
        nuevo_municipio = self.repo_crear.crear(municipio)
        return nuevo_municipio
