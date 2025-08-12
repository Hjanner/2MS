from typing import List, Optional, TypeVar, Generic, Dict, Any
from fastapi import HTTPException
from backend.models.view_models import ProductoVistaBase, ProductoVistaNoPreparado, ProductoVistaPreparado
from backend.services.base_service import DuplicateKeyError

T = TypeVar('T')  # Modelo Pydantic

class BaseController(Generic[T]):
    """
    Clase base genérica para controladores CRUD.
    Permite reutilizar la lógica de orquestación de servicios para cualquier entidad.
    """
    def __init__(self, service):
        """
        Inicializa el controlador con el servicio correspondiente.
        :param service: Instancia de BaseService para la entidad.
        """
        self.service = service

    def get_all(self) -> List[T]:
        """
        Obtiene todos los registros de la entidad.
        :return: Lista de instancias del modelo.
        """
        return self.service.get_all()

    def get_by_id(self, id_field: str, id_value) -> Optional[T]:
        """
        Obtiene un registro por su campo clave primaria.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :return: Instancia del modelo o None si no existe.
        """
        return self.service.get_by_id(id_field, id_value)

    def get_by_keys(self, keys: Dict[str, Any]) -> Optional[T]:
        """
        Obtiene un registro por múltiples campos clave (clave primaria compuesta).
        :param keys: Diccionario con los campos clave y sus valores.
        :return: Instancia del modelo o None si no existe.
        """
        return self.service.get_by_keys(keys)

    def create(self, obj_in: T) -> Any:
        """
        Crea un nuevo registro en la entidad.
        :param obj_in: Instancia del modelo a crear.
        :raises HTTPException: 409 si hay duplicados, 400 para otros errores.
        """
        try:
            return self.service.create(obj_in)

        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": e.message,
                    "field": e.field,
                    "value": e.value,
                    "code": "DUPLICATE_KEY"
                }
            )
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=400,
        #         detail={
        #             "message": f"Error al crear el registro: {str(e)}",
        #             "code": "CREATE_ERROR"
        #         }
        #     )

    def update(self, id_field: str, id_value, obj_in: T) -> bool:
        """
        Actualiza un registro existente.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :param obj_in: Instancia del modelo con los nuevos datos.
        :return: True si se actualizó, False si no existe.
        """
        return self.service.update(id_field, id_value, obj_in)

    def update_by_keys(self, keys: Dict[str, Any], obj_in: T) -> bool:
        """
        Actualiza un registro existente usando múltiples campos clave.
        :param keys: Diccionario con los campos clave y sus valores.
        :param obj_in: Instancia del modelo con los nuevos datos.
        :return: True si se actualizó, False si no existe.
        """
        return self.service.update_by_keys(keys, obj_in)

    def delete(self, id_field: str, id_value) -> bool:
        """
        Elimina un registro por su campo clave primaria.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :return: True si se eliminó, False si no existe.
        """
        return self.service.delete(id_field, id_value)

    def delete_by_keys(self, keys: Dict[str, Any]) -> bool:
        """
        Elimina un registro usando múltiples campos clave.
        :param keys: Diccionario con los campos clave y sus valores.
        :return: True si se eliminó, False si no existe.
        """
        return self.service.delete_by_keys(keys)
    
    async def create_with_file(self, obj_in) -> Any:
        """
        Crea un nuevo registro con archivo adjunto.
        :param obj_in: Instancia del modelo con archivo
        :raises HTTPException: 409 si hay duplicados, 400 para otros errores
        """
        try:
            if hasattr(self.service, 'create_with_file'):
                return await self.service.create_with_file(obj_in)
            return self.service.create(obj_in)
        except DuplicateKeyError as e:
            raise HTTPException(status_code=409, detail={
                "message": e.message,
                "field": e.field,
                "value": e.value
            })

    def get_producto_completo(self) -> List[ProductoVistaBase]:
        productos_data = self.service.get_productos_completos()
        productos = []
        
        for prod in productos_data:
            if prod['tipo_producto'] == 'preparado':
                productos.append(ProductoVistaPreparado(**prod))
            elif prod['tipo_producto'] == 'noPreparado':
                productos.append(ProductoVistaNoPreparado(**prod))
            else:
                productos.append(ProductoVistaBase(**prod))
        
        return productos

    def get_last_record(self, id_field: str ) -> Any:
        return self.service.get_last_record(id_field)