from typing import Optional, Union, List
from pydantic import BaseModel, Field
from .models import Compra, Proveedor, Producto, ProductoNoPreparado, Movimiento


class ProductoVistaBase(BaseModel):
    cod_producto: str = Field(..., description="Código único del producto")
    nombre: str = Field(..., description="Nombre del producto")
    precio_usd: float = Field(..., description="Precio en dólares")
    id_categoria: Optional[int] = Field(None, description="ID de categoría")
    img: Optional[str] = Field(None, description="URL de la imagen")
    categoria_descr: Optional[str] = Field(None, description="Descripción de la categoría")
    categoria_tipo: Optional[str] = Field(None, description="Tipo de categoría")
    tipo_producto: str = Field(..., description="Tipo de producto (preparado/noPreparado)")

class ProductoVistaPreparado(ProductoVistaBase):
    descr_preparado: Optional[str] = Field(None, description="Descripción del producto preparado")

class ProductoVistaNoPreparado(ProductoVistaBase):
    cant_min: Optional[int] = Field(None, description="Cantidad mínima en inventario")
    cant_actual: Optional[int] = Field(None, description="Cantidad actual en inventario")
    costo_compra: Optional[float] = Field(None, description="Costo de compra")
    unidad_medida: Optional[str] = Field(None, description="Unidad de medida")
    Rif: Optional[str] = Field(None, description="RIF del proveedor")
    
ProductoVista = Union[ProductoVistaPreparado, ProductoVistaNoPreparado, ProductoVistaBase]

#MODELO DE VISTA PARA DETALLES DE COMPRA
class DetalleProductoCompra(BaseModel):
    """Modelo que combina información de producto y su detalle en la compra"""
    producto: Producto
    producto_no_preparado: ProductoNoPreparado
    movimiento: Movimiento
    
class DetalleCompra(BaseModel):
    """Modelo completo para el detalle de una compra"""
    compra: Compra
    proveedor: Proveedor
    productos: List[DetalleProductoCompra]
    fecha_formateada: str = Field(..., description="Fecha formateada como DD/MM/YYYY")

class ResumenCompra(BaseModel):
    """Modelo para resumen de compra (sin detalles de productos)"""
    compra: Compra
    proveedor: Proveedor
    cantidad_productos: int = Field(..., description="Cantidad de productos diferentes en la compra")
    fecha_formateada: str = Field(..., description="Fecha formateada como DD/MM/YYYY")