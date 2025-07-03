from core.entidades.descuento import Descuento
from datetime import datetime
from core.interfaces.repositorioDescuento import CrearDescuentoProtocol, ObtenerDescuentoPorIdProtocol
from core.servicios.descuentos.dtos import CrearDescuentoDTO


class CrearDescuento:
    def __init__(self, repo_crear: CrearDescuentoProtocol, repo_obtener: ObtenerDescuentoPorIdProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearDescuentoDTO) -> Descuento:
        descuento = Descuento(
            id_usuario=datos.id_usuario,
            id_cuenta_por_pagar=datos.id_cuenta_por_pagar,
            id_deuda=datos.id_deuda,
            valor=datos.valor,
            fecha_creacion=datetime.now(),
            tipo_de_descuento=datos.tipo_de_descuento,
            descripcion=datos.descripcion,
            fecha_actualizacion=datetime.now(),
        )
        if descuento.id:
            descuento_existente = self.repo_obtener.obtener_descuento_por_id(descuento.id)
            if descuento_existente:
                return descuento_existente

        descuento = self.repo_crear.crear(descuento)

        return descuento
