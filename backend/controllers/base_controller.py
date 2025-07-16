from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')  # Modelo Pydantic

class BaseController(Generic[T]):
    """
    Clase base genérica para controladores
    """
    def __init__(self, service):
        self.service = service

    def get_all(self) -> List[T]:
        return self.service.get_all()

    def get_by_id(self, id_field: str, id_value) -> Optional[T]:
        return self.service.get_by_id(id_field, id_value)

    def create(self, obj_in: T) -> None:
        self.service.create(obj_in)

    def update(self, id_field: str, id_value, obj_in: T) -> bool:
        return self.service.update(id_field, id_value, obj_in)

    def delete(self, id_field: str, id_value) -> bool:
        return self.service.delete(id_field, id_value)