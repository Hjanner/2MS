from fastapi import APIRouter, HTTPException
from typing import Type, List

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