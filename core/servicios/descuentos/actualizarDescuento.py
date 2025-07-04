from app.api.esquemas.descuento import ActualizarDescuentoSchema
from core.interfaces.repositorioDescuento import ActualizarDescuentoProtocol, ObtenerDescuentoPorIdProtocol

# from core.servicios.descuentos.dtos import ActualizarDescuentoDTO


class ActualizarDescuento:
    def __init__(self, repo_actualizar: ActualizarDescuentoProtocol, repo_obtener: ObtenerDescuentoPorIdProtocol):
        self.repo_actualizar = repo_actualizar
        self.repo_obtener = repo_obtener

    def ejecutar(self, id_descuento: int, data_descuento: ActualizarDescuentoSchema):
        descuento_existente = self.repo_obtener.obtener_descuento_por_id(id_descuento)

        if not descuento_existente:
            raise ValueError(f"Descuento con ID {id_descuento} no encontrado.")

        if data_descuento.valor is not None:
            descuento_existente.actualizar_valor(data_descuento.valor)
        if data_descuento.descripcion is not None:
            descuento_existente.actualizar_descripcion(data_descuento.descripcion)
        if data_descuento.tipo_de_descuento is not None:
            descuento_existente.actualizar_tipo_de_descuento(data_descuento.tipo_de_descuento)

        return self.repo_actualizar.actualizar(descuento_existente)
