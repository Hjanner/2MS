from fastapi import APIRouter, HTTPException
from typing import Type, List

def create_crud_router(
    entity_name: str,
    controller,
    id_field: str,
    model: Type,
    tag: str = None
):
    router = APIRouter(prefix=f"/{entity_name}", tags=[tag or entity_name.capitalize()])

    @router.get("/", response_model=List[model])
    def getAll():
        return controller.get_all()

    @router.get("/{item_id}", response_model=model)
    def get(item_id: str):
        obj = controller.get_by_id(id_field, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return obj

    @router.post("/", response_model=None, status_code=201)
    def create(obj_in: model):
        controller.create(obj_in)
        return {"mensaje": f"{entity_name.capitalize()} creado exitosamente"}

    @router.put("/{item_id}", response_model=None)
    def update(item_id: str, obj_in: model):
        actualizado = controller.update(id_field, item_id, obj_in)
        if not actualizado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} actualizado exitosamente"}

    @router.delete("/{item_id}", response_model=None)
    def delete(item_id: str):
        eliminado = controller.delete(id_field, item_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail=f"{entity_name.capitalize()} no encontrado")
        return {"mensaje": f"{entity_name.capitalize()} eliminado exitosamente"}

    return router