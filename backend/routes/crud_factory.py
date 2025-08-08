import inspect
from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Depends
from typing import Any, Dict, Type, List, Optional, Union

from backend.utilities.get_data import get_form_data_as_dict

def create_crud_router(
    entity_name: str,
    controller,
    id_field: str,
    model: Type,
    tag: str = None,
    *,
    with_file_upload: bool = False,
    file_field: str = 'img',
    create_model: Optional[Type] = None
):
    """
    Fábrica de routers CRUD genéricos para FastAPI.
    Genera endpoints estándar para cualquier entidad usando un controller base.
    :param entity_name: Nombre de la entidad (usado en el prefijo de la ruta).
    :param controller: Instancia de BaseController para la entidad.
    :param id_field: Nombre del campo clave primaria.
    :param model: Clase del modelo Pydantic.
    :param tag: Nombre del tag para la documentación (opcional).
    :param: with_file_upload: Si True, añade endpoints para manejar archivos
    :param: file_field: Nombre del campo que contendrá el archivo
    :param: create_model: Modelo específico para creación (opcional)
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
    

    if with_file_upload:
        # Obtenemos los campos del modelo para crear los parámetros del Form
        model_fields = {}
        if create_model:
            model_fields = create_model.__annotations__
        else:
            model_fields = model.__annotations__
        
        # Eliminamos el campo de archivo ya que lo manejamos por separado
        form_fields = {k: v for k, v in model_fields.items() if k != file_field}
        
        # Creamos una dependencia dinámica para los campos del formulario
        async def get_form_data(
            **fields: Any  # Los campos se generarán dinámicamente
        ):
            return fields

        # Generamos los parámetros del Form dinámicamente
        form_parameters = []
        for field_name, field_type in form_fields.items():
            default = ... if field_name in model.__fields__ and model.__fields__[field_name].required else None
            annotation = field_type if field_type != UploadFile else str
            form_parameters.append(
                inspect.Parameter(
                    field_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Form(default) if annotation != File else File(default),
                    default=default
                )
            )

        # Actualizamos la firma de la función para incluir los campos dinámicos
        original_signature = inspect.signature(get_form_data)
        new_parameters = list(original_signature.parameters.values()) + form_parameters
        get_form_data.__signature__ = original_signature.replace(parameters=new_parameters)

        @router.post("/with-file", status_code=201)
        async def create_with_file(
            file: UploadFile = File(..., alias=file_field),
            form_data: Dict[str, Any] = Depends(get_form_data)
        ):
            # Combina los datos del formulario con el archivo
            data = {**form_data, file_field: file}
            
            if create_model:
                obj_in = create_model(**data)
            else:
                obj_in = model(**data)
                
            if hasattr(controller, 'create_with_file'):
                result = await controller.create_with_file(obj_in)
            else:
                result = controller.create(obj_in)
                
            return {"mensaje": f"{entity_name.capitalize()} creado con archivo", "data": result}

        return router

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