from core.entidades.departamento import Departamento
from core.interfaces.repositorioDepartamento import (
    ObtenerDepartamentoPorNombreProtocol,
    CrearDepartamentoProtocol,
)
from core.servicios.departamento.ObtenerDepartamento import ObtenerDepartamento
from .dtos import CrearDepartamentoDTO, ObtenerDepartamentoDTO


class CrearDepartamento:
    def __init__(self, repo_obtener: ObtenerDepartamentoPorNombreProtocol, repo_crear: CrearDepartamentoProtocol):
        self.repo_obtener = repo_obtener
        self.repo_crear = repo_crear

    async def ejecutar(self, datos: CrearDepartamentoDTO) -> Departamento:
        try:
            departamento_obtenido = await ObtenerDepartamento(self.repo_obtener).ejecutar(
                ObtenerDepartamentoDTO(nombre=datos.nombre)
            )
            return departamento_obtenido
        except ValueError:
            nuevo_departamento = await self.repo_crear.crear(Departamento(nombre=datos.nombre))
            return nuevo_departamento
