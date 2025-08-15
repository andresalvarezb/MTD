from core.entidades.departamento import Departamento
from core.interfaces.repositorioDepartamento import ObtenerDepartamentoPorNombreProtocol

from .dtos import ObtenerDepartamentoDTO


class ObtenerDepartamento:
    def __init__(self, repo_obtener: ObtenerDepartamentoPorNombreProtocol):
        self.repo_obtener = repo_obtener

    async def ejecutar(self, datos: ObtenerDepartamentoDTO) -> Departamento:

        # buscar departamento por nombre
        departamento_obtenido = await self.repo_obtener.obtener_por_nombre(datos.nombre)
        if not departamento_obtenido:
            raise ValueError("Departamento no existe. Puede estar mal escrito o no creado")

        return departamento_obtenido
