from fastapi import APIRouter, Depends
from infraestructura.db.index import get_db
from sqlalchemy.orm import Session
from app.api.esquemas.area import CrearAreaMTDSchema
from app.api.esquemas.area import AreaMTDResponseSchema
from core.servicios.areaMTD.crearAreaMTD import CrearAreaMTD
from core.servicios.areaMTD.obtenerAreasMTD import ObtenerAreasMTD
from core.servicios.areaMTD.obtenerAreaMTD import ObtenerAreaMTD
from core.servicios.areaMTD.eliminarAreaMTD import EliminarAreaMTD
from infraestructura.db.repositorios.repositorioAreaSqlAlchemy import RepositorioAreaMTDSqlAlchemy








router = APIRouter()


@router.post("/", response_model=AreaMTDResponseSchema)
def crear_area(data_area: CrearAreaMTDSchema, db: Session = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    caso_de_uso = CrearAreaMTD(repo_obtener=repo_area, repo_crear=repo_area)
    area = caso_de_uso.ejecutar(data_area.nombre)
    db.commit()
    return AreaMTDResponseSchema.model_validate(area)

@router.get("", response_model=list[AreaMTDResponseSchema])
def obtener_areas(db: Session = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    areas = ObtenerAreasMTD(repo_area).ejecutar()
    return [AreaMTDResponseSchema.model_validate(area) for area in areas]

@router.get("/{id_area}", response_model=AreaMTDResponseSchema)
def obtener_area(id_area: int, db: Session = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    caso_de_uso = ObtenerAreaMTD(repo_area)
    area = caso_de_uso.ejecutar(id_area)
    return AreaMTDResponseSchema.model_validate(area)

@router.delete("/{id_area}")
def eliminar_area(id_area: int, db: Session = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    caso_de_uso = EliminarAreaMTD(repo_area)
    if not caso_de_uso.ejecutar(id_area):
        db.commit()
        return {"mensaje": "Area eliminada correctamente"}