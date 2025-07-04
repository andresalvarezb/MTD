from core.entidades.deuda import Deuda
from core.interfaces.repositorioDeuda import CrearDeudaProtocol
from core.servicios.deudas.dtos import CrearDeudaDTO
from core.interfaces.repositorioUsuario import ObtenerUsuarioPorDocumentoProtocol
from decimal import Decimal
from datetime import datetime
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
        # validar usuario al que se le asigna la deuda
        area_deuda = None
        usuario = self.repo_usuario.obtener_por_documento(datos.documento)

        if not usuario:
            raise ValueError(f"Usuario {datos.documento} no encontrado. No se puede asignar deuda")

        # validar monto de la deuda
        if datos.monto <= 0 or datos.monto == None:
            raise ValueError("El monto de la deuda debe ser mayor a cero")

        # si le asignan un area, validar que esta exista
        if datos.area:
            area = self.repo_area.obtener_por_nombre(datos.area)
            if not area:
                raise ValueError(f"Area {datos.area} no encontrada. No se puede asignar deuda")

            area_deuda = area

        # crear deuda

        deuda = Deuda(
            usuario=usuario,
            estado="PENDIENTE",
            saldo=datos.monto,
            valor_total=datos.monto,
            descripcion=datos.descripcion,
            area=area_deuda,
        )

        deuda = self.repo_deuda.crear(deuda)

        return deuda

        # if usuario.id is None:
        #     raise KeyError(f"El usuario no esta agregado a un en la base de datos.")
