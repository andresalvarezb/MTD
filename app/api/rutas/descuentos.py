from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from app.api.esquemas.descuento import DescuentoResponseSchema, ActualizarDescuentoSchema
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO, CrearDescuentoDTO
from core.servicios.descuentos.obtenerDescuentos import ObtenerDescuentos
from core.servicios.descuentos.obtenerDescuento import ObtenerDescuento
from infraestructura.db.repositorios.repositorioDescuentoSQLAlchemy import RepositorioDescuentoSqlAlchemy
from app.api.esquemas.descuento import CrearDescuentoSchema
from core.servicios.descuentos.crearDescuento import CrearDescuento
from core.servicios.descuentos.actualizarDescuento import ActualizarDescuento
from core.servicios.descuentos.eliminarDescuento import EliminarDescuento


router = APIRouter()


@router.get("/", response_model=list[DescuentoResponseSchema])
async def obtener_descuentos(
    id_cuenta_por_pagar: int | None = Query(
        None, description="id de la cuenta por pagar en la que se aplica el descuento"
    ),
    id_usuario: int | None = Query(None, description="id del usuario al que le aplica el descuento"),
    id_deuda: int | None = Query(None, description="id de la deuda en la que se aplica el descuento"),
    db: Session = Depends(get_db),
):
    try:
        repo_descuento = RepositorioDescuentoSqlAlchemy(db)
        caso_de_uso = ObtenerDescuentos(repo_descuento)
        descuentos = caso_de_uso.ejecutar(
            FiltrarDescuentosDTO(id_cuenta_por_pagar=id_cuenta_por_pagar, id_usuario=id_usuario, id_deuda=id_deuda)
        )
        descuentos_response = [DescuentoResponseSchema.model_validate(descuento) for descuento in descuentos]
        return descuentos_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{id_descuento}", response_model=DescuentoResponseSchema)
async def obtener_descuento(id_descuento: int, db: Session = Depends(get_db)):
    try:
        repo_descuento = RepositorioDescuentoSqlAlchemy(db)
        caso_de_uso = ObtenerDescuento(repo_descuento)
        descuento = caso_de_uso.ejecutar(id_descuento)
        descuento_response = DescuentoResponseSchema.model_validate(descuento)
        return descuento_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/", response_model=DescuentoResponseSchema)
def crear_descuento(data_descuento: CrearDescuentoSchema, db: Session = Depends(get_db)):
    repo_descuento = RepositorioDescuentoSqlAlchemy(db)
    caso_de_uso = CrearDescuento(
        repo_crear=repo_descuento,
        repo_obtener=repo_descuento,
    )
    descuento = caso_de_uso.ejecutar(
        CrearDescuentoDTO(
            id_cuenta_por_pagar=data_descuento.id_cuenta_por_pagar,
            id_usuario=data_descuento.id_usuario,
            id_deuda=data_descuento.id_deuda,
            valor=data_descuento.valor,
            fecha_actualizacion=data_descuento.fecha_actualizacion,
            fecha_creacion=data_descuento.fecha_creacion,
            tipo_de_descuento=data_descuento.tipo_de_descuento,
            descripcion=data_descuento.descripcion,
        )
    )
    return DescuentoResponseSchema.model_validate(descuento)


@router.patch("/{id_descuento}", response_model=DescuentoResponseSchema)
def actualizar_descuento(data_descuento: ActualizarDescuentoSchema, id_descuento: int, db: Session = Depends(get_db)):
    repo_descuento = RepositorioDescuentoSqlAlchemy(db)
    caso_de_uso = ActualizarDescuento(repo_actualizar=repo_descuento, repo_obtener=repo_descuento)
    descuento = caso_de_uso.ejecutar(id_descuento, data_descuento)
    return DescuentoResponseSchema.model_validate(descuento)


@router.delete("/{id_descuento}")
def eliminar_descuento(
    id_descuento: int = Path(..., description="ID del descuento a eliminar"), db: Session = Depends(get_db)
):
    try:
        repo_descuento = RepositorioDescuentoSqlAlchemy(db)
        caso_de_uso = EliminarDescuento(repo_eliminar=repo_descuento)
        caso_de_uso.ejecutar(id_descuento)
        return {"message": "Descuento eliminado correctamente"}
    except:
        raise HTTPException(status_code=500, detail="Error interno al eliminar el descuento")
