from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime
from backend.models.view_models import DetalleVentaCompleto, ResumenVenta, DetalleProductoVenta

class VistaVentasController:
    def __init__(self, service):
        self.service = service

    def obtener_detalle_venta(self, id_venta: int) -> DetalleVentaCompleto:
        """
        Obtiene el detalle completo de una venta por su ID
        """
        try:
            detalle = self.service.obtener_detalle_venta(id_venta)
            if not detalle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Venta con ID {id_venta} no encontrada"
                )
            return detalle
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener detalle de venta: {str(e)}"
            )

    def listar_ventas(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        ci_cliente: Optional[str] = None,
        tipo_venta: Optional[str] = None,
        metodo_pago: Optional[str] = None,
        limit: int = 100
    ) -> List[ResumenVenta]:
        """
        Lista resúmenes de ventas con filtros opcionales
        """
        try:
            # Validar formatos de fecha si se proporcionan
            if fecha_inicio:
                datetime.strptime(fecha_inicio, "%d/%m/%Y")
            if fecha_fin:
                datetime.strptime(fecha_fin, "%d/%m/%Y")
            
            return self.service.obtener_resumenes_ventas(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                ci_cliente=ci_cliente,
                tipo_venta=tipo_venta,
                metodo_pago=metodo_pago,
                limit=limit
            )
        except ValueError as e:
            if "time data" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Formato de fecha inválido. Use DD/MM/YYYY"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al listar ventas: {str(e)}"
            )

    def obtener_ventas_por_producto(
        self,
        cod_producto: str,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 100
    ) -> List[DetalleProductoVenta]:
        """
        Obtiene todas las ventas donde aparece un producto específico
        """
        try:
            # Validar formatos de fecha si se proporcionan
            if fecha_inicio:
                datetime.strptime(fecha_inicio, "%d/%m/%Y")
            if fecha_fin:
                datetime.strptime(fecha_fin, "%d/%m/%Y")
            
            ventas = self.service.obtener_ventas_por_producto(
                cod_producto=cod_producto,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                limit=limit
            )
            
            if not ventas:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontraron ventas para el producto {cod_producto}"
                )
                
            return ventas
        except ValueError as e:
            if "time data" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Formato de fecha inválido. Use DD/MM/YYYY"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except HTTPException:
            raise  # Re-lanzamos las HTTPException que ya hemos capturado
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener ventas por producto: {str(e)}"
            )