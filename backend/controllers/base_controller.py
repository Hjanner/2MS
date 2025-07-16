from typing import List, Optional, TypeVar, Generic

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

    def create(self, obj_in: T) -> None:
        """
        Crea un nuevo registro en la entidad.
        :param obj_in: Instancia del modelo a crear.
        """
        self.service.create(obj_in)

    def update(self, id_field: str, id_value, obj_in: T) -> bool:
        """
        Actualiza un registro existente.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :param obj_in: Instancia del modelo con los nuevos datos.
        :return: True si se actualizó, False si no existe.
        """
        return self.service.update(id_field, id_value, obj_in)

    def delete(self, id_field: str, id_value) -> bool:
        """
        Elimina un registro por su campo clave primaria.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :return: True si se eliminó, False si no existe.
        """
        return self.service.delete(id_field, id_value)