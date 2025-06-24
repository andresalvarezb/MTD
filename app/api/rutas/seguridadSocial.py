from fastapi import APIRouter, HTTPException, Depends
from infraestructura.db.index import get_db
from sqlalchemy.orm import Session
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from infraestructura.db.repositorios.repositorioHistorialLaboralUsuarioSqlAlchemy import (
    RepositorioHistorialLaboralUsuarioSqlAlchemy,
)
from core.servicios.historialLaboral.actualizarSeguridadSocial import ActualizarSeguridadSocial
from app.api.esquemas.seguridadSocial import ActualizacionSeguridadSocialSchema

router = APIRouter()


@router.patch(
    "/",
)
def actualizar_seguridad_social(data: ActualizacionSeguridadSocialSchema, db: Session = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        repo_historialLaboralUsuario = RepositorioHistorialLaboralUsuarioSqlAlchemy(db)
        caso_de_uso = ActualizarSeguridadSocial(
            obtener_usuario_repo=repo_usuario,
            obtener_hlu_repo=repo_historialLaboralUsuario,
            actualizar_ss_usuario_repo=repo_usuario,
            actualizar_ss_hlu_repo=repo_historialLaboralUsuario,
        )
        usuario, historial_laboral = caso_de_uso.ejecutar(data)
        db.commit()

        return {
            "mensaje": "Seguridad social actualizada correctamente",
            "usuario": usuario,
            "historial_laboral": historial_laboral,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
