from typing import Optional, Union
from pydantic import BaseModel, Field

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
