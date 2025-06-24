from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from fastapi import APIRouter, HTTPException, Depends
from core.servicios.descuentos.obtenerDescuento import ObtenerDescuento
from core.servicios.descuentos.obtenerDescuentos import ObtenerDescuentos
from app.api.esquemas.descuento import DescuentoResponseSchema
from infraestructura.db.repositorios.repositorioDescuentoSQLAlchemy import RepositorioDescuentoSqlAlchemy


router = APIRouter()


@router.get("/", response_model=list[DescuentoResponseSchema])
async def obtener_descuentos(db: Session = Depends(get_db)):
    try:
        repo_descuento = RepositorioDescuentoSqlAlchemy(db)
        caso_de_uso = ObtenerDescuentos(repo_descuento)
        descuentos = caso_de_uso.ejecutar()
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
