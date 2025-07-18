import sqlite3
from typing import Type, List, Optional, Any, Dict

class BaseService:
    """
    Plantilla reusable para interactuar con cualquier tabla de tu base de datos,
    siempre y cuando esa tabla esté asociada a un modelo Pydantic
    (o similar) que tenga los métodos to_dict() y from_dict().
    
    Permite operaciones CRUD reutilizables para cualquier entidad,
    solo necesitas pasar el modelo, el nombre de la tabla y la ruta de la base de datos.
    """
    
    def __init__(self, model: Type, table_name: str, db_path: str):
        """
        Inicializa el servicio base para una entidad.
        :param model: Clase del modelo Pydantic.
        :param table_name: Nombre de la tabla en la base de datos.
        :param db_path: Ruta al archivo de la base de datos.
        """
        self.model = model
        self.table_name = table_name
        self.db_path = db_path

    def get_all(self) -> List[Any]:
        """
        Obtiene todos los registros de la tabla.
        :return: Lista de instancias del modelo.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return [self.model.from_dict(dict(zip([col[0] for col in cursor.description], row))) for row in rows]

    def get_by_id(self, id_field: str, id_value: Any) -> Optional[Any]:
        """
        Obtiene un registro por su campo clave primaria.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :return: Instancia del modelo o None si no existe.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {id_field} = ?", (id_value,))
            row = cursor.fetchone()
            if row:
                return self.model.from_dict(dict(zip([col[0] for col in cursor.description], row)))
            return None

    def get_by_keys(self, keys: Dict[str, Any]) -> Optional[Any]:
        """
        Obtiene un registro por múltiples campos clave (clave primaria compuesta).
        :param keys: Diccionario con los campos clave y sus valores.
        :return: Instancia del modelo o None si no existe.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            where_clause = " AND ".join([f"{k} = ?" for k in keys.keys()])
            values = tuple(keys.values())
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {where_clause}", values)
            row = cursor.fetchone()
            if row:
                return self.model.from_dict(dict(zip([col[0] for col in cursor.description], row)))
            return None

    def create(self, obj_in) -> Any:
        """
        Inserta un nuevo registro en la tabla.
        :param obj_in: Instancia del modelo a insertar.
        """
        data = obj_in.to_dict()
        fields = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})",
                values
            )
            conn.commit()
        return data

    def update(self, id_field: str, id_value: Any, obj_in) -> bool:
        """
        Actualiza un registro existente en la tabla.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :param obj_in: Instancia del modelo con los nuevos datos.
        :return: True si se actualizó, False si no existe.
        """
        data = obj_in.to_dict()
        fields = ', '.join([f"{k} = ?" for k in data.keys() if k != id_field])
        values = tuple([v for k, v in data.items() if k != id_field]) + (id_value,)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {self.table_name} SET {fields} WHERE {id_field} = ?",
                values
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_by_keys(self, keys: Dict[str, Any], obj_in) -> bool:
        """
        Actualiza un registro existente usando múltiples campos clave.
        :param keys: Diccionario con los campos clave y sus valores.
        :param obj_in: Instancia del modelo con los nuevos datos.
        :return: True si se actualizó, False si no existe.
        """
        data = obj_in.to_dict()
        # Excluir los campos clave del update
        update_fields = [f"{k} = ?" for k in data.keys() if k not in keys]
        update_values = [v for k, v in data.items() if k not in keys]
        
        where_clause = " AND ".join([f"{k} = ?" for k in keys.keys()])
        where_values = tuple(keys.values())
        
        all_values = tuple(update_values) + where_values
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE {where_clause}",
                all_values
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, id_field: str, id_value: Any) -> bool:
        """
        Elimina un registro por su campo clave primaria.
        :param id_field: Nombre del campo clave primaria.
        :param id_value: Valor del campo clave primaria.
        :return: True si se eliminó, False si no existe.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE {id_field} = ?",
                (id_value,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_by_keys(self, keys: Dict[str, Any]) -> bool:
        """
        Elimina un registro usando múltiples campos clave.
        :param keys: Diccionario con los campos clave y sus valores.
        :return: True si se eliminó, False si no existe.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            where_clause = " AND ".join([f"{k} = ?" for k in keys.keys()])
            values = tuple(keys.values())
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE {where_clause}",
                values
            )
            conn.commit()
            return cursor.rowcount > 0 