from sqlalchemy.ext.asyncio import AsyncSession
from core.entidades.usuario import Usuario
from infraestructura.db.index import get_db
from fastapi import APIRouter, HTTPException, Depends, Query
from core.servicios.usuarios.obtenerUsuario import ObtenerUsuario
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.servicios.usuarios.obtenerUsuarios import ObtenerUsuarios
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from app.api.esquemas.usuario import UsuarioCreateSchema, UsuarioResponseSchema, UsuarioUpdateSchema
from core.servicios.usuarios.dtos import CrearUsuarioDTO


router = APIRouter()

@router.post("/", response_model=UsuarioResponseSchema)
async def crear_usuario(usuario: UsuarioCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = CrearUsuario(repo_usuario, repo_usuario)
        usuario_creado = await caso_de_uso.ejecutar(CrearUsuarioDTO(**usuario.model_dump()))
        return usuario_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/", response_model=list[UsuarioResponseSchema])
async def obtener_usuarios(
    documento: str | None = Query(None, description="Filtrar por documento de un usuario en particular"),
    db: AsyncSession = Depends(get_db),
):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuarios(repo_usuario)
        usuarios = await caso_de_uso.ejecutar(documento)
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{id_usuario}", response_model=UsuarioResponseSchema)
async def obtener_un_usuario(id_usuario: int, db: AsyncSession = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuario(repo_usuario)
        usuarios = await caso_de_uso.ejecutar(id_usuario)
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
