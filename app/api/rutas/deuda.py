from infraestructura.db.index import get_db
from sqlalchemy.ext.asyncio import AsyncSession
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
async def crear_deuda(deuda: CrearDeudaSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        repo_area = RepositorioAreaMTDSqlAlchemy(db)
        caso_de_uso = CrearDeuda(repo_deuda=repo_deuda, obtener_usuario_repo=repo_usuario, obtener_area_repo=repo_area)
        deuda_creada = await caso_de_uso.ejecutar(CrearDeudaDTO(**deuda.model_dump()))
        await db.commit()
        return DeudaRespuestaSchema.model_validate(deuda_creada)

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=list[DeudaRespuestaSchema], summary="Obtener todas las deudas")
async def obtener_deudas(db: AsyncSession = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = ObtenerDeudas(repo_deuda)
        deudas = await caso_de_uso.ejecutar()
        return [DeudaRespuestaSchema.model_validate(deuda) for deuda in deudas]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.patch("/{id_deuda}", response_model=DeudaRespuestaSchema)
async def actualizar_deuda(id_deuda: int, deuda_actualizada: ActualizarDeudaSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = ActualizarDeuda(repo_actualizar=repo_deuda, repo_obtener=repo_deuda)
        deuda = await caso_de_uso.ejecutar(id_deuda, info_nueva=deuda_actualizada)
        await db.commit()
        return DeudaRespuestaSchema.model_validate(deuda)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{id_deuda}")
async def eliminar_deuda(
    id_deuda: int = Path(..., title="ID de la deuda a eliminar"), db: AsyncSession = Depends(get_db)
):
    try:
        repo_deuda = RepositorioDeudaSqlAlchemy(db)
        caso_de_uso = EliminarDeuda(repo_deuda)
        await caso_de_uso.ejecutar(id_deuda)
        await db.commit()
        return {"mensaje": "Deuda eliminada correctamente"}
    except ValueError as ve:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
