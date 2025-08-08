from fastapi import APIRouter
from ..controllers.view_controllers import VistaProductosController
from ..models.view_models import ProductoVista
from typing import List
from database.database import db_path

router = APIRouter(
    prefix="/vista",
    tags=["Vistas"]
)

controller = VistaProductosController(db_path)

@router.get("/productos-completos", response_model=List[ProductoVista])
def get_productos_completos():
    """
    Obtiene todos los productos con información completa combinada
    """
    return controller.get_all()