from fastapi import APIRouter, HTTPException
from typing import Type, List, Dict, Any

def create_crud_router(
    entity_name: str,
    controller,
    id_field: str,
    model: Type,
    tag: str = None
):
    """
    Fábrica de routers CRUD genéricos para FastAPI.
    Genera endpoints estándar para cualquier entidad usando un controller base.
    :param entity_name: Nombre de la entidad (usado en el prefijo de la ruta).
    :param controller: Instancia de BaseController para la entidad.
    :param id_field: Nombre del campo clave primaria.
    :param model: Clase del modelo Pydantic.
    :param tag: Nombre del tag para la documentación (opcional).
    :return: APIRouter listo para incluir en la app.
    """
    router = APIRouter(prefix=f"/{entity_name}", tags=[tag or entity_name.capitalize()])

    @router.get("/", response_model=List[model])
    def getAll():
        """Obtiene todos los registros de la entidad."""
        return controller.get_all()

    @router.get("/{item_id}", response_model=model)
    def get(item_id: str):
        """Obtiene un registro por su clave primaria."""
        obj = controller.get_by_id(id_field, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return obj

    @router.post("/", response_model=None, status_code=201)
    def create(obj_in: model):
        """Crea un nuevo registro de la entidad."""
        controller.create(obj_in)
        return {"mensaje": f"{entity_name.capitalize()} creado exitosamente"}

    @router.put("/{item_id}", response_model=None)
    def update(item_id: str, obj_in: model):
        """Actualiza un registro existente de la entidad."""
        actualizado = controller.update(id_field, item_id, obj_in)
        if not actualizado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} actualizado exitosamente"}

    @router.delete("/{item_id}", response_model=None)
    def delete(item_id: str):
        """Elimina un registro de la entidad por su clave primaria."""
        eliminado = controller.delete(id_field, item_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} eliminado exitosamente"}

    return router

def create_composite_crud_router(
    entity_name: str,
    controller,
    key_fields: List[str],
    model: Type,
    tag: str = None
):
    """
    Fábrica de routers CRUD genéricos para entidades con claves primarias compuestas.
    Genera endpoints estándar para entidades que usan múltiples campos como clave primaria.
    :param entity_name: Nombre de la entidad (usado en el prefijo de la ruta).
    :param controller: Instancia de BaseController para la entidad.
    :param key_fields: Lista de nombres de los campos que forman la clave primaria.
    :param model: Clase del modelo Pydantic.
    :param tag: Nombre del tag para la documentación (opcional).
    :return: APIRouter listo para incluir en la app.
    """
    router = APIRouter(prefix=f"/{entity_name}", tags=[tag or entity_name.capitalize()])

    # Crear la ruta con múltiples parámetros
    route_params = "/".join([f"{{{field}}}" for field in key_fields])
    
    @router.get("/", response_model=List[model])
    def getAll():
        """Obtiene todos los registros de la entidad."""
        return controller.get_all()

    @router.get(f"/{route_params}", response_model=model)
    def get(**kwargs):
        """Obtiene un registro por sus campos clave primaria compuesta."""
        obj = controller.get_by_keys(kwargs)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return obj

    @router.post("/", response_model=None, status_code=201)
    def create(obj_in: model):
        """Crea un nuevo registro de la entidad."""
        controller.create(obj_in)
        return {"mensaje": f"{entity_name.capitalize()} creado exitosamente"}

    @router.put(f"/{route_params}", response_model=None)
    def update(obj_in: model, **kwargs):
        """Actualiza un registro existente de la entidad usando clave primaria compuesta."""
        actualizado = controller.update_by_keys(kwargs, obj_in)
        if not actualizado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} actualizado exitosamente"}

    @router.delete(f"/{route_params}", response_model=None)
    def delete(**kwargs):
        """Elimina un registro de la entidad usando clave primaria compuesta."""
        eliminado = controller.delete_by_keys(kwargs)
        if not eliminado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} eliminado exitosamente"}

    return router