from fastapi import APIRouter, Depends
from infraestructura.db.index import get_db
from sqlalchemy.orm import Session
from app.api.esquemas.area import CrearAreaMTDSchema
from core.servicios.areaMTD.crearAreaMTD import CrearAreaMTD
from infraestructura.db.repositorios.repositorioAreaSqlAlchemy import RepositorioAreaMTDSqlAlchemy
from app.api.esquemas.area import AreaMTDResponseSchema






router = APIRouter()


@router.post("/", response_model=AreaMTDResponseSchema)
def crear_area(data_area: CrearAreaMTDSchema, db: Session = Depends(get_db)):
    repo_area = RepositorioAreaMTDSqlAlchemy(db)
    caso_de_uso = CrearAreaMTD(repo_obtener=repo_area, repo_crear=repo_area)
    area = caso_de_uso.ejecutar(data_area.nombre)
    db.commit()
    return AreaMTDResponseSchema.model_validate(area)