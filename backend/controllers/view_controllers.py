from math import log
from typing import List
from ..services.view_services import VistaService
from ..models.view_models import ProductoVistaBase, ProductoVistaPreparado, ProductoVistaNoPreparado

class VistaProductosController:
    def __init__(self, db_path: str):
        self.service = VistaService(db_path)
    
    def get_all(self) -> List[ProductoVistaBase]:
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