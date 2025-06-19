from core.entidades.descuento import Descuento
from core.interfaces.repositorioDescuento import RepositorioDescuento


class CrearDescuento:
    def __init__(self, repositorio: RepositorioDescuento):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Descuento:
        descuento = Descuento(
            id_cuenta_por_pagar=datos["id_cuenta_por_pagar"],
            id_usuario=datos["id_usuario"],
            id_deuda=datos["id_deuda"],
            valor=datos["valor"],
            fecha_creacion=datos["fecha_creacion"],
            tipo_de_descuento=datos["tipo_de_descuento"],
            descripcion=datos["descripcion"],
            fecha_actualizacion=datos["fecha_actualizacion"],
        )
        descuento = self.repositorio.guardar(descuento)

        return descuento
