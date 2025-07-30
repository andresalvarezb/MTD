from core.entidades.departamento import Departamento
from core.interfaces.repositorioDepartamento import (
    ObtenerDepartamentoPorNombreProtocol,
    CrearDepartamentoProtocol,
)

from .dtos import CrearDepartamentoDTO


class CrearDepartamento:
    def __init__(self, repo_departamento):
        self.repo_obtener: ObtenerDepartamentoPorNombreProtocol = repo_departamento
        self.repo_crear: CrearDepartamentoProtocol = repo_departamento

    async def ejecutar(self, datos: CrearDepartamentoDTO) -> Departamento:
        departamento = Departamento(nombre=datos.nombre)

        # buscar departamento por nombre
        existe_departamento = await self.repo_obtener.obtener_por_nombre(departamento)
        if existe_departamento:
            return existe_departamento

        # crearlo de no existir
        nuevo_departamento = await self.repo_crear.crear(departamento)
        return nuevo_departamento