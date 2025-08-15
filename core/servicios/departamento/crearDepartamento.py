from core.entidades.departamento import Departamento
from core.interfaces.repositorioDepartamento import (
    ObtenerDepartamentoPorNombreProtocol,
    CrearDepartamentoProtocol,
)
from core.servicios.departamento.ObtenerDepartamento import ObtenerDepartamento
from .dtos import CrearDepartamentoDTO, ObtenerDepartamentoDTO
from core.servicios.utilities.exepciones import DepartamentoNoExisteError


class CrearDepartamento:
    def __init__(self, obtener_departamento: ObtenerDepartamento, repo_crear: CrearDepartamentoProtocol):
        self.obtener_departamento = obtener_departamento
        self.repo_crear = repo_crear

    async def ejecutar(self, datos: CrearDepartamentoDTO) -> Departamento:
        try:
            return await self.obtener_departamento.ejecutar(
                ObtenerDepartamentoDTO(nombre=datos.nombre)
            )
        except DepartamentoNoExisteError:
            return await self.repo_crear.crear(Departamento(nombre=datos.nombre))