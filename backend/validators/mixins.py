from pydantic import field_validator
from .common import *

class ClienteValidators:
    @field_validator('ci_cliente')
    @classmethod
    def validate_ci_cliente(cls, v):
        v = validate_only_digits(v, "Cédula")
        return validate_max_length(v, 10, "Cédula")

    @field_validator('tlf')
    @classmethod
    def validate_tlf(cls, v):
        if v is not None:
            return validate_phone(v, "Teléfono")
        return v

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v):
        return validate_name(v, "Nombre")


class ProveedorValidators:
    """Mixin con validaciones específicas para proveedores"""
    
    @field_validator('Rif')
    @classmethod
    def validate_rif(cls, v):
        return validate_rif(v)

    @field_validator('tfl')
    @classmethod
    def validate_tfl(cls, v):
        if v is not None:
            v = validate_starts_with(v, ['0', '+58'], "Teléfono")
            if len(v) < 10:
                raise ValueError('El teléfono debe tener al menos 10 dígitos')
        return v

class ProductoValidators:
    """Mixin con validaciones específicas para productos"""
    
    @field_validator('cod_producto')
    @classmethod
    def validate_cod_producto(cls, v):
        v = validate_not_empty(v, "Código de producto")
        return v.upper()

    @field_validator('precio')
    @classmethod
    def validate_precio(cls, v):
        return validate_positive_number(v, "Precio")

class VentaValidators:
    """Mixin con validaciones específicas para ventas"""
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        return validate_enum(v, ['credito', 'de_contado'], "Tipo de venta")

    @field_validator('monto_total_bs')
    @classmethod
    def validate_monto(cls, v):
        return validate_positive_number(v, "Monto total (Bs)")
    
class TasaCambioValidators:
    @field_validator('valor_usd_bs')
    @classmethod
    def validate_valor_usd_bs(cls, v):
        return validate_positive_number(v, "Tasa")

    @field_validator('origen')
    @classmethod
    def validate_origen(cls, v):
        return validate_enum(v, ['BCV', 'Manual'], "Origen")

class CategoriaProductoValidators:
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        return validate_enum(v, ['preparado', 'noPreparado'], "Tipo")


class ProductoPreparadoValidators:
    @field_validator('descr')
    @classmethod
    def validate_descr(cls, v):
        v = validate_not_empty(v, "Descripción")
        return v.title()


class ProductoNoPreparadoValidators:
    @field_validator('cant_min', 'cant_actual', 'costo_compra')
    @classmethod
    def validate_numericos(cls, v, field):
        return validate_non_negative_number(v, field.name)

    @field_validator('unidad_medida')
    @classmethod
    def validate_unidad(cls, v):
        v = validate_not_empty(v, "Unidad de medida")
        return v.lower()


class PagoValidators:
    @field_validator('metodo_pago')
    @classmethod
    def validate_metodo(cls, v):
        metodos_validos = [
            'efectivo_bs', 'efectvo_usd',
            'pago_movil', 'debito', 'transferencia'
        ]
        return validate_enum(v, metodos_validos, "Método de pago")

    @field_validator('monto')
    @classmethod
    def validate_monto(cls, v):
        return validate_positive_number(v, "Monto")


class InventarioValidators:
    @field_validator('referencia')
    @classmethod
    def validate_referencia(cls, v):
        referencias_validas = [
            'compra', 'venta', 'descarte', 'ajuste',
            'traslado_tienda', 'autoconsumo'
        ]
        return validate_enum(v, referencias_validas, "Referencia")

    @field_validator('tipo_movimiento')
    @classmethod
    def validate_tipo_mov(cls, v):
        return validate_enum(v, ['entrada', 'salida'], "Tipo de movimiento")

    @field_validator('cant_movida')
    @classmethod
    def validate_cant(cls, v):
        return validate_positive_number(v, "Cantidad movida")


class DetalleVentaValidators:
    @field_validator('cantidad_producto', 'precio_unitario')
    @classmethod
    def validate_detalle(cls, v, field):
        return validate_positive_number(v, field.name)


class CompraInventarioValidators:
    @field_validator('cant_comprada', 'monto_unitario')
    @classmethod
    def validate_compra(cls, v, field):
        return validate_positive_number(v, field.name)