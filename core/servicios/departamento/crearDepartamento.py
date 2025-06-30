from core.entidades.departamento import Departamento
from core.interfaces.repositorioDepartamento import (
    ObtenerDepartamentoPorNombreProtocol,
    CrearDepartamentoProtocol,
)

from .dtos import CrearDepartamentoDTO


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
