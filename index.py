import uvicorn
from app.api.index import app

# 👇 Importa dinámicamente todos los modelos definidos
from infraestructura.db.modelos import (
    municipio,
    areaMTD,
    deuda,
    # ... importa todos tus otros modelos aquí para que Base los reconozca
)


@app.get("/")
async def root():
    return {"message": "Pagina principal"}


if __name__ == "__main__":
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
