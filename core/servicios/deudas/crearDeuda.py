from core.entidades.deuda import Deuda
from core.interfaces.repositorioDeuda import CrearDeudaProtocol
from core.servicios.deudas.dtos import CrearDeudaDTO
from core.interfaces.repositorioUsuario import ObtenerUsuarioPorDocumentoProtocol
from decimal import Decimal
from core.interfaces.repositorioAreaMTD import ObtenerAreaPorNombreProtocol


class CrearDeuda:
    def __init__(
        self,
        repo_deuda: CrearDeudaProtocol,
        obtener_usuario_repo: ObtenerUsuarioPorDocumentoProtocol,
        obtener_area_repo: ObtenerAreaPorNombreProtocol,
    ):
        self.repo_deuda = repo_deuda
        self.repo_usuario = obtener_usuario_repo
        self.repo_area = obtener_area_repo

    def ejecutar(self, datos: CrearDeudaDTO) -> Deuda:
        usuario = self.repo_usuario.obtener_por_documento(datos.documento)

        if not usuario:
            raise ValueError(f"Usuario {datos.documento} no encontrado. No se puede asignar deuda")

        # ! Revisar el bug que genera esta linea. se agrega este parche pero es un comportamiento inesperado
        if usuario.id is None:
            raise KeyError(f"El usuario no esta agregado a un en la base de datos.")

        if datos.monto <= 0:
            raise ValueError("El monto de la deuda debe ser mayor a cero")

        area = self.repo_area.obtener_por_nombre(datos.area)
        if not area:
            raise ValueError(f"Area {datos.area} no encontrada. No se puede asignar deuda")

        deuda = Deuda(
            id_usuario=usuario.id,
            estado="PENDIENTE",
            saldo=datos.monto,
            valor_total=datos.monto,
            fecha_creacion=datos.fecha_creacion,
            descripcion=datos.descripcion,
            id_area=area.id,
        )

        deuda = self.repo_deuda.crear(deuda)

        return deuda
