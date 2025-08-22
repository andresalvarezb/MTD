from fastapi import APIRouter, Depends, HTTPException, status, Path
from infraestructura.db.index import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.esquemas.area import CrearAreaMTDSchema
from app.api.esquemas.area import AreaMTDResponseSchema
from core.servicios.areaMTD.crearAreaMTD import CrearAreaMTD
from core.servicios.areaMTD.obtenerAreasMTD import ObtenerAreasMTD
from core.servicios.areaMTD.eliminarAreaMTD import EliminarAreaMTD
from infraestructura.db.repositorios.repositorioAreaSqlAlchemy import RepositorioAreaMTDSqlAlchemy


router = APIRouter()


@router.post("/", response_model=AreaMTDResponseSchema)
async def crear_area(data_area: CrearAreaMTDSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_area = RepositorioAreaMTDSqlAlchemy(db)
        caso_de_uso = CrearAreaMTD(
            repo_obtener=ObtenerAreasMTD(repo_area, repo_area),
            repo_crear=repo_area
        )
        area = await caso_de_uso.ejecutar(data_area.nombre)
        await db.commit()
        return AreaMTDResponseSchema.model_validate(area)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[AreaMTDResponseSchema])
async def obtener_areas(db: AsyncSession = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    areas = await ObtenerAreasMTD(repo_area, repo_area).ejecutar()
    return [AreaMTDResponseSchema.model_validate(area) for area in areas]


@router.get("/{id_area}", response_model=AreaMTDResponseSchema)
async def obtener_area(id_area: int = Path(
        ...,
        title="Id Area MTD",
        description="Identificador unico de la Area MTD",
        gt=0,
        examples=["0", "1", "2"],
    ), db: AsyncSession = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    caso_de_uso = ObtenerAreasMTD(repo_area, repo_area)
    area = await caso_de_uso.ejecutar(id_area)
    return AreaMTDResponseSchema.model_validate(area)


@router.delete("/{id_area}")
async def eliminar_area(id_area: int, db: AsyncSession = Depends(get_db)):
    try:
        repo_area = RepositorioAreaMTDSqlAlchemy(db)
        caso_de_uso = EliminarAreaMTD(repo_area)
        await caso_de_uso.ejecutar(id_area)
        await db.commit()
        return {"mensaje": "Area eliminada correctamente"}
    except ValueError as ve:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
