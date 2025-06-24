from sqlalchemy.orm import Session
from core.entidades.usuario import Usuario
from infraestructura.db.index import get_db
from fastapi import APIRouter, HTTPException, Depends
from core.servicios.usuarios.obtenerUsuario import ObtenerUsuario
from core.servicios.usuarios.obtenerUsuarios import ObtenerUsuarios
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy


router = APIRouter()


@router.get("/", response_model=list[Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuarios(repo_usuario)
        usuarios = caso_de_uso.ejecutar()
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{id_usuario}", response_model=Usuario)
def obtener_un_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuario(repo_usuario)
        usuarios = caso_de_uso.ejecutar(id_usuario)
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
