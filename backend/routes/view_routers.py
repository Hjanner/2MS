from fastapi import APIRouter
from ..models.view_models import DetalleCompra, ProductoVista, ResumenCompra
from typing import List
from backend.controllers.controller import vistaProductosController, vistaComprasController

router = APIRouter(
    prefix="/vista",
    tags=["Vistas"]
)


@router.get("/productos-completos", response_model=List[ProductoVista])
def get_productos_completos():
    """
    Obtiene todos los productos con información completa combinada
    """
    return vistaProductosController.get_producto_completo()



@router.get( "/{id_compra}/detalle", response_model=DetalleCompra,
    summary="Obtener detalle completo de una compra",
    description="""Obtiene todos los detalles de una compra específica incluyendo:
    - Información de la compra
    - Datos del proveedor
    - Lista de productos con sus detalles completos
    - Movimientos de inventario asociados""",
    responses={
        200: {"description": "Detalle de compra obtenido exitosamente"},
        404: {"description": "Compra no encontrada"}
    }
)
def get_detalle_compra(id_compra: int):
    return vistaComprasController.obtener_detalle_compra(id_compra)

# @router.get(
#     "/",
#     response_model=List[ResumenCompra],
#     summary="Listar resúmenes de compras",
#     description="""Obtiene un listado de resúmenes de compras con capacidad de filtrado.
#     Cada resumen incluye:
#     - Información básica de la compra
#     - Datos del proveedor
#     - Cantidad de productos en la compra""",
#     responses={
#         200: {"description": "Listado de compras obtenido exitosamente"}
#     }
# )
# return controller.listar_compras(