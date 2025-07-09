from core.entidades.descuento import Descuento
from datetime import datetime
from core.interfaces.repositorioDescuento import CrearDescuentoProtocol, ObtenerDescuentoPorIdProtocol
from core.servicios.descuentos.dtos import CrearDescuentoDTO
from core.interfaces.repositorioCuentaPorPagar import ObtenerCuentaPorPagarPorIdProtocol, ActualizarCuentaPorPagarProtocol


class CrearDescuento:
    # def __init__(self, repo_crear: CrearDescuentoProtocol, repo_obtener_descuento: ObtenerDescuentoPorIdProtocol):
    #     self.repo_crear = repo_crear
    #     self.repo_obtener = repo_obtener

    def __init__(self, repo_descuento, repo_cuenta):
        self.repo_crear_descuento: CrearDescuentoProtocol = repo_descuento
        self.repo_obtener_descuento: ObtenerDescuentoPorIdProtocol = repo_descuento
        self.repo_obtener_cuenta: ObtenerCuentaPorPagarPorIdProtocol = repo_cuenta
        self.repo_actualizar_cuenta: ActualizarCuentaPorPagarProtocol = repo_cuenta

    def ejecutar(self, datos: CrearDescuentoDTO) -> Descuento:
        descuento = self._crear_descuento(datos)

        # * Actualización cuenta por pagar
        self._actualizar_cuenta_por_pagar(descuento)

        return descuento

    def _crear_descuento(self, datos: CrearDescuentoDTO) -> Descuento:
        descuento = Descuento(
            id_usuario=datos.id_usuario,
            id_cuenta_por_pagar=datos.id_cuenta_por_pagar,
            id_deuda=datos.id_deuda,
            valor=datos.valor,
            fecha_creacion=datetime.now() if not datos.fecha_creacion else datos.fecha_creacion,
            tipo_de_descuento=datos.tipo_de_descuento,
            descripcion=datos.descripcion,
            fecha_actualizacion=datetime.now(),
        )
        if descuento.id:
            descuento_existente = self.repo_obtener_descuento.obtener_descuento_por_id(descuento.id)
            if descuento_existente:
                return descuento_existente

        descuento = self.repo_crear_descuento.crear(descuento)
        return descuento

    def _actualizar_cuenta_por_pagar(self, descuento: Descuento):
        """Actualización del total a pagar y el total de descuentos"""
        cuenta_por_pagar = self.repo_obtener_cuenta.obtener_por_id(descuento.id_cuenta_por_pagar)
        if not cuenta_por_pagar:
            raise ValueError(f"Cuenta por pagar con id {descuento.id_cuenta_por_pagar} no encontrada")

        cuenta_por_pagar.calcular_descuentos([descuento])
        cuenta_por_pagar.total_descuentos = cuenta_por_pagar.total_descuentos
        cuenta_por_pagar.total_a_pagar = cuenta_por_pagar.total_a_pagar

        self.repo_actualizar_cuenta.actualizar(cuenta_por_pagar)