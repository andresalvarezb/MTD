import uvicorn
from fastapi import FastAPI
from app.api.index import router as api_router
from infraestructura.db.index import Base, engine

# 👇 Importa dinámicamente todos los modelos definidos
import infraestructura.db.modelos.municipio
import infraestructura.db.modelos.deuda

app = FastAPI(title="API Cuentas Medicas", description="", version="0.1.0")
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Pagina principal"}


# 👇 Esto crea todas las tablas si no existen
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
