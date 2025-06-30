from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from app.api.esquemas.deuda import CrearDeudaSchema
from app.api.esquemas.deuda import DeudaRespuestaSchema
from core.servicios.deudas.crearDeuda import CrearDeuda
from core.servicios.deudas.obtenerDeudas import ObtenerDeudas
from fastapi import APIRouter, HTTPException, Depends, status
from infraestructura.db.repositorios.repositorioDeudaSqlAlchemy import RepositorioDeudaSqlAlchemy
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from infraestructura.db.repositorios.repositorioAreaSqlAlchemy import RepositorioAreaMTDSqlAlchemy


router = APIRouter()


@router.post(
    "/crear",
    response_model=DeudaRespuestaSchema,
    summary="Crear nueva deuda asociada a un usuario",
    status_code=status.HTTP_201_CREATED,
)
def crear_deuda(deuda: CrearDeudaSchema, db: Session = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        repo_area = RepositorioAreaMTDSqlAlchemy(db)
        caso_de_uso = CrearDeuda(repo_deuda=repo_deuda, obtener_usuario_repo=repo_usuario, obtener_area_repo=repo_area)
        deuda_creada = caso_de_uso.ejecutar(**deuda.model_dump())
        db.commit()
        return DeudaRespuestaSchema.model_validate(deuda_creada)

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=list[DeudaRespuestaSchema], summary="Obtener todas las deudas")
def obtener_deudas(db: Session = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = ObtenerDeudas(repo_deuda)
        deudas = caso_de_uso.ejecutar()
        return [DeudaRespuestaSchema.model_validate(deuda) for deuda in deudas]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
