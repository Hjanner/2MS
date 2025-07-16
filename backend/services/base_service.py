import sqlite3
from typing import Type, List, Optional, Any

class BaseService:
    """
    Plantilla reusable para interactuar con cualquier tabla de tu base de datos, 
    siempre y cuando esa tabla esté asociada a un modelo Pydantic 
    (o similar) que tenga los métodos to_dict() y from_dict().
    
    Permite operaciones CRUD reutilizables para cualquier entidad, 
    solo necesitas pasar el modelo, el nombre de la tabla y la ruta de la base de datos.
    """
    
    def __init__(self, model: Type, table_name: str, db_path: str):
        self.model = model
        self.table_name = table_name
        self.db_path = db_path

    def get_all(self) -> List[Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return [self.model.from_dict(dict(zip([col[0] for col in cursor.description], row))) for row in rows]

    def get_by_id(self, id_field: str, id_value: Any) -> Optional[Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE {id_field} = ?", (id_value,))
            row = cursor.fetchone()
            if row:
                return self.model.from_dict(dict(zip([col[0] for col in cursor.description], row)))
            return None

    def create(self, obj_in) -> None:
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

    def update(self, id_field: str, id_value: Any, obj_in) -> bool:
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

    def delete(self, id_field: str, id_value: Any) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE {id_field} = ?",
                (id_value,)
            )
            conn.commit()
            return cursor.rowcount > 0 