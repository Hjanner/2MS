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

from backend.routes.routes import clientes_router, proveedores_router
app.include_router(clientes_router)
app.include_router(proveedores_router)
