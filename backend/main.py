import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from routes import items
from fastapi.middleware.cors import CORSMiddleware

with open("tags_metadata.json") as f:
    tags_metadata = json.load(f)

app = FastAPI(
    title="2MS API", 
    description="API for Morela's Cafe",
    version="0.1",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.routes.routes import *
app.include_router(clientes_router)
app.include_router(proveedores_router)
app.include_router(productos_router)
app.include_router(ventas_router)
app.include_router(tasasCambio_router)
app.include_router(categoria_productos_router)
app.include_router(compras_router)
app.include_router(creditos_router)
app.include_router(pagos_router)
app.include_router(inventarios_router)
app.include_router(detalle_venta_router)
app.include_router(compra_inventario_router)
app.include_router(productos_preparados_router)
app.include_router(productos_noPreparados_router)
