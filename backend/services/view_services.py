from typing import List, Type, Dict, Any
import sqlite3
from ..models.view_models import *

class VistaService:
    """
    Servicio especializado para consultas de vistas complejas
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_productos_completos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos con información completa desde la vista
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vista_productos_completos")
            return [dict(row) for row in cursor.fetchall()]