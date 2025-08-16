from fastapi import HTTPException, status
from typing import Optional, List
from datetime import date
from backend.models.view_models import DetalleCompra, ResumenCompra

class VistaComprasController:
    def __init__(self, service):
        self.service = service

    def obtener_detalle_compra(self, id_compra: int,) -> DetalleCompra:
        try:
            detalle = self.service.obtener_detalle_compra(id_compra)
            if not detalle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Compra con ID {id_compra} no encontrada"
                )
            return detalle
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def listar_compras(
        self, 
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        rif_proveedor: Optional[str] = None,
        limit: int = 100,
    ) -> List[ResumenCompra]:
        try:
            return self.service.obtener_resumenes_compras(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                rif_proveedor=rif_proveedor,
                limit=limit
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )