import uvicorn
from app.api.index import app
from infraestructura.db.index import Base, async_engine
from contextlib import asynccontextmanager
# 👇 Importa dinámicamente todos los modelos definidos
from infraestructura.db.modelos import (
    municipio,
    areaMTD,
    deuda,
    # ... importa todos tus otros modelos aquí para que Base los reconozca
)


@asynccontextmanager
async def lifespan(app):
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Opcional: para borrar todo al reiniciar
        await conn.run_sync(Base.metadata.create_all)
    yield
        # await async_engine.dispose() # Código de cierre (opcional)


@app.get("/")
async def root():
    return {"message": "Pagina principal"}

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
