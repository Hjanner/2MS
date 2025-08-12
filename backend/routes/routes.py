# Aquí se crean los controladores y routers para cada entidad usando la fábrica genérica

from fastapi import HTTPException
from fastapi.params import Depends
from backend.models.models import *
from backend.controllers.controller import *
from backend.models.view_models import DetalleProductoVenta, DetalleVentaCompleto, ResumenVenta
from backend.services.transactions.venta_transactions import registrar_venta_con_detalles_y_pago
from .crud_factory import create_crud_router

# Creación de routers CRUD genéricos para cada entidad
clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)
productos_router = create_crud_router("productos", productos_controller, "cod_producto", Producto, with_file_upload=True, file_field='img', create_model=ProductoCreate)
ventas_router = create_crud_router("ventas", ventas_controller, "id_ventas", Venta)
tasasCambio_router = create_crud_router("tasas_cambio", tasasCambio_controller, "id_tasa", TasaCambio)
categoria_productos_router = create_crud_router("categoria_productos", categoria_productos_controller, "id_categoria", CategoriaProducto)
compras_router = create_crud_router("compras", compras_controller, "id_compra", Compra)
creditos_router = create_crud_router("creditos", creditos_controller, "id_credito", Credito)
pagos_router = create_crud_router("pagos", pagos_controller, "id_pago", Pago)
movimientos_router = create_crud_router("movimientos", movimientos_controller, "id_movimiento", Movimiento)
detalle_venta_router = create_crud_router("detalle_venta", detalle_venta_controller, "id_detalle", DetalleVenta)
productos_preparados_router = create_crud_router("productos_preparados", productos_preparados_controller, "cod_producto_preparado", ProductoPreparado)
productos_noPreparados_router = create_crud_router("productos_noPreparados", productos_noPreparados_controller, "cod_producto_noPreparado", ProductoNoPreparado)



@productos_router.put("/{cod_producto}", response_model=None)
def update(cod_producto: str, producto: Producto):
    print("Actualizando producto:", cod_producto, producto)
    updated = productos_controller.update("cod_producto", cod_producto, producto)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

#endpoint para registrar una venta
@ventas_router.post("/registrar")
def registrar_venta(payload: VentaTransaccionPayload):
    try:
        result = registrar_venta_con_detalles_y_pago(
            venta_data=payload.venta,
            detalles_data=payload.detalles,
            pago_data=payload.pago,
            db_path=db_path
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Error interno del servidor",
                "message": str(e)
            }
        )


@tasasCambio_router.get("/ultima_tasa/", response_model=Any)
def get_last_record():
    print("Obteniendo última tasa actualizada:")
    ultima_tasa = tasasCambio_controller.get_last_record("id_tasa")
    if not ultima_tasa:
        raise HTTPException(status_code=404, detail="Tasa de cambio no encontrada")
    return ultima_tasa

@ventas_router.get("/detalle/{id_venta}", response_model=DetalleVentaCompleto)
def get_sale_detail(id_venta: int):
    try:
        detalle = vistaVentasController.obtener_detalle_venta(id_venta)
        return detalle
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener detalle de venta: {str(e)}"
        )

@ventas_router.get("/listar/", response_model=List[ResumenVenta])
def list_ventas(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    ci_cliente: Optional[str] = None,
    tipo_venta: Optional[str] = None,
    metodo_pago: Optional[str] = None,
    limit: int = 100
):
    try:
        return vistaVentasController.listar_ventas(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            ci_cliente=ci_cliente,
            tipo_venta=tipo_venta,
            metodo_pago=metodo_pago,
            limit=limit
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener lista de venta: {str(e)}"
        )
        
# @ventas_router.get("/producto/{cod_producto}", response_model=List[DetalleProductoVenta])
# async def buscar_ventas_por_producto(
#     cod_producto: str,
#     fecha_inicio: Optional[str] = None,
#     fecha_fin: Optional[str] = None,
#     limit: int = 100,
#     service: VentaDetalleService = Depends(get_venta_service)
# ):
#     controller = VistaVentasController(service)
#     return controller.obtener_ventas_por_producto(
#         cod_producto=cod_producto,
#         fecha_inicio=fecha_inicio,
#         fecha_fin=fecha_fin,
#         limit=limit
#     )

