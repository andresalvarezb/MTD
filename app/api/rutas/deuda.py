from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from app.api.esquemas.deuda import CrearDeudaSchema, ActualizarDeudaSchema
from app.api.esquemas.deuda import DeudaRespuestaSchema
from core.servicios.deudas.crearDeuda import CrearDeuda
from core.servicios.deudas.obtenerDeudas import ObtenerDeudas
from fastapi import APIRouter, HTTPException, Depends, status, Path
from infraestructura.db.repositorios.repositorioDeudaSqlAlchemy import RepositorioDeudaSqlAlchemy
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from infraestructura.db.repositorios.repositorioAreaSqlAlchemy import RepositorioAreaMTDSqlAlchemy
from core.servicios.deudas.actualizarDeuda import ActualizarDeuda
from core.servicios.deudas.eliminarDeuda import EliminarDeuda
from core.servicios.deudas.dtos import CrearDeudaDTO

router = APIRouter()


@router.post(
    "/",
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
        deuda_creada = caso_de_uso.ejecutar(CrearDeudaDTO(**deuda.model_dump()))
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


@router.patch("/{id_deuda}", response_model=DeudaRespuestaSchema)
def actualizar_deuda(id_deuda: int, deuda_actualizada: ActualizarDeudaSchema, db: Session = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = ActualizarDeuda(repo_actualizar=repo_deuda, repo_obtener=repo_deuda)
        deuda = caso_de_uso.ejecutar(id_deuda, info_nueva=deuda_actualizada)
        db.commit()
        return DeudaRespuestaSchema.model_validate(deuda)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{id_deuda}")
def eliminar_deuda(id_deuda: int = Path(..., title="ID de la deuda a eliminar"), db: Session = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = EliminarDeuda(repo_deuda)
        caso_de_uso.ejecutar(id_deuda)
        db.commit()
        return {"mensaje": "Deuda eliminada correctamente"}
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        db.rollback()
        return {"mensaje": f"Error interno: {str(e)}"}
