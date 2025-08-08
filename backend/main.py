import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes.pydolarve_routers import api_utils_router
from backend.routes.view_routers import router as vista_router

import backend.utilities.apscheduler as scheduler_config
from contextlib import asynccontextmanager


with open("tags_metadata.json") as f:
    tags_metadata = json.load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not scheduler_config.scheduler.running:
        scheduler_config.scheduler.start()
        print("Scheduler iniciado exitosamente.")
    yield
    if scheduler_config.scheduler.running:
        scheduler_config.scheduler.shutdown()
        print("Scheduler apagado.")

app = FastAPI(
    title="2MS API", 
    description="API for Morela's Cafe",
    version="0.1",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["*http://localhost:3000"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")            #para servir la imagenes


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
app.include_router(productos_preparados_router)
app.include_router(productos_noPreparados_router)

app.include_router(api_utils_router)

app.include_router(vista_router)
