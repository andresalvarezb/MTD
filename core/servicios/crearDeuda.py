from core.entidades.deuda import Deuda
from core.interfaces.repositorioDeuda import RepositorioDeuda


class Creardeuda:
    def __init__(self, repositorio: RepositorioDeuda):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Deuda:
        deuda = Deuda(
            id_usuario=datos["id_usuario"],
            estado=datos["estado"],
            saldo=datos["saldo"],
            valor_total=datos["valor_total"],
            fecha_creacion=datos["fecha_creacion"],
            fecha_actualizacion=datos["fecha_actualizacion"],
            id_area=datos["id_area"],
        )

        deuda = self.repositorio.guardar(deuda)

        return deuda