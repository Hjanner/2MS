from datetime import datetime
import os
import sqlite3
from typing import Type, List, Optional, Any, Dict
import uuid

async def create_with_file(self, obj_in, file_field: str = 'img', upload_dir: str = 'public/uploads') -> Any:
    """
    Crea un registro con un archivo adjunto.
    :param obj_in: Datos del objeto
    :param file_field: Nombre del campo del archivo
    :param upload_dir: Directorio donde guardar los archivos
    :return: Datos del objeto creado
    """
    data = obj_in.model_dump(exclude={file_field})
    file = getattr(obj_in, file_field, None)
    
    self._check_unique_constraints(data)        # Verificar restricciones de unicidad
    
    if file:                                        # Guardar archivo si existe
        os.makedirs(upload_dir, exist_ok=True)
        file_ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, 'wb') as buffer:                                   # Guardar el archivo
            buffer.write(await file.read())
        
        data[file_field] = f"/{upload_dir}/{filename}"
    
    fields = ', '.join(data.keys())                                         # Insertar en la base de datos
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values())
    
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})",
                values
            )
            conn.commit()
            return data
    except sqlite3.IntegrityError as e:
        # Limpiar archivo subido si hubo error
        if file and os.path.exists(file_path):
            os.remove(file_path)
        raise DuplicateKeyError("unknown", "unknown", str(e))


class DuplicateKeyError(Exception):
    """Excepción personalizada para claves duplicadas."""
    def __init__(self, field: str, value: Any, message: str = None):
        self.field = field
        self.value = value
        self.message = message or f"Ya existe un registro con {field} = {value}"
        super().__init__(self.message)


class BaseService:
    """
    Plantilla reusable para interactuar con cualquier tabla de tu base de datos,
    siempre y cuando esa tabla esté asociada a un modelo Pydantic
    (o similar) que tenga los métodos to_dict() y from_dict().
    
    Permite operaciones CRUD reutilizables para cualquier entidad,
    solo necesitas pasar el modelo, el nombre de la tabla y la ruta de la base de datos.
    """
    
    def __init__(self, model: Type, table_name: str, db_path: str, unique_fields: List[str] = None):
        """
        Inicializa el servicio base para una entidad.
        :param model: Clase del modelo Pydantic.
        :param table_name: Nombre de la tabla en la base de datos.
        :param db_path: Ruta al archivo de la base de datos.
        """
        self.model = model
        self.table_name = table_name
        self.db_path = db_path
        self.unique_fields = unique_fields or []


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

    def _check_unique_constraints(self, obj_data: Dict[str, Any], exclude_id: Any = None) -> None:
        """
        Verifica las restricciones de unicidad antes de crear/actualizar.
        :param obj_data: Datos del objeto a verificar.
        :param exclude_id: ID a excluir en la verificación (para updates).
        :raises DuplicateKeyError: Si encuentra un duplicado.
        """
        for field in self.unique_fields:
            if field in obj_data:
                value = obj_data[field]
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Query base para verificar duplicados
                    query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {field} = ?"
                    params = [value]
                    
                    # Si es un update, excluir el registro actual
                    if exclude_id is not None:
                        # Asumimos que el primer campo único es la primary key
                        pk_field = self.unique_fields[0] if self.unique_fields else field
                        query += f" AND {pk_field} != ?"
                        params.append(exclude_id)
                    
                    cursor.execute(query, params)
                    count = cursor.fetchone()[0]
                    
                    if count > 0:
                        raise DuplicateKeyError(field, value)

    def create(self, obj_in) -> Any:
        """
        Inserta un nuevo registro en la tabla.
        :param obj_in: Instancia del modelo a insertar.
        :raises DuplicateKeyError: Si viola restricciones de unicidad.
        """
        data = obj_in.to_dict()
        
        # Verificar restricciones de unicidad
        self._check_unique_constraints(data)
        
        fields = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})",
                    values
                )
                conn.commit()
        except sqlite3.IntegrityError as e:
            # Manejar errores de integridad de SQLite
            error_msg = str(e).lower()
            
            # Intentar identificar qué campo causó el error
            for field in self.unique_fields:
                if field.lower() in error_msg:
                    raise DuplicateKeyError(field, data.get(field))
            
            # Si no podemos identificar el campo específico
            raise DuplicateKeyError("unknown", "unknown", "Error de integridad: registro duplicado")
        
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

    def get_last_record(self, id_field: str) -> Optional[Any]:
        """
        Obtiene el último registro de la tabla.
        :param id_field: Nombre del campo clave primaria para ordenar.
        :return: Instancia del modelo o None si la tabla está vacía.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY {id_field} DESC LIMIT 1")
            
            row = cursor.fetchone()
            if row:
                return self.model.from_dict(dict(zip([col[0] for col in cursor.description], row)))
            return None
        
#VISTAS
    def get_productos_completos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos con información completa desde la vista
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vista_productos_completos")
            return [dict(row) for row in cursor.fetchall()]

#FILTROS
    def get_data_from_date(
        self, 
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        ) -> List[Any]:
        """
        Obtiene los datos filtrados por rango de fechas.
        :return: Lista de instancias del modelo o lista vacía si no hay datos.
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []
        
        conditions = []
        
        if fecha_inicio:
            conditions.append("fecha >= ?")
            params.append(datetime.strptime(fecha_inicio, "%d/%m/%Y").isoformat())
        
        if fecha_fin:
            conditions.append("fecha <= ?")
            params.append(datetime.strptime(fecha_fin, "%d/%m/%Y").isoformat())
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY fecha DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if rows:
                # Crear una lista de objetos del modelo
                return [self.model.from_dict(dict(row)) for row in rows]
            return []  # Retornar lista vacía en lugar de None

            
            