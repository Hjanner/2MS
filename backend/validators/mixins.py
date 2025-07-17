from pydantic import field_validator
from typing import Optional

class ClienteValidators:
    """Mixin con validaciones específicas para clientes"""
    
    @field_validator('ci_cliente')
    @classmethod
    def validate_ci_cliente(cls, v):
        """Valida formato de cédula venezolana"""
        if not v.isdigit():
            raise ValueError('La cédula debe contener solo números')
        if len(v) > 10:
            raise ValueError('La cédula supera los 10 dígitos')
        return v

    @field_validator('tlf')
    @classmethod
    def validate_tlf(cls, v):
        """Valida formato de teléfono venezolano"""
        if v is not None:
            if not v.startswith('0'):
                raise ValueError('El teléfono debe comenzar con 0')
            if len(v) != 11:
                raise ValueError('El teléfono debe tener exactamente 11 dígitos')
            if not v.isdigit():
                raise ValueError('El teléfono debe contener solo números')
        return v

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, v):
        """Valida formato de nombre"""
        if any(char.isdigit() for char in v):
            raise ValueError('El nombre no puede contener números')
        return v.title()  # Capitalizar nombre

class ProveedorValidators:
    """Mixin con validaciones específicas para proveedores"""
    
    @field_validator('Rif')
    @classmethod
    def validate_rif(cls, v):
        """Valida formato de RIF venezolano"""
        if not v.startswith(('V', 'E', 'J', 'P', 'G')):
            raise ValueError('El RIF debe comenzar con V, E, J, P o G')
        if len(v) < 9:
            raise ValueError('El RIF debe tener al menos 9 caracteres')
        return v.upper()

    @field_validator('tfl')
    @classmethod
    def validate_tfl(cls, v):
        """Valida formato de teléfono de proveedor"""
        if v is not None:
            if not v.startswith(('0', '+58')):
                raise ValueError('El teléfono debe comenzar con 0 o +58')
            if len(v) < 10:
                raise ValueError('El teléfono debe tener al menos 10 dígitos')
        return v

class ProductoValidators:
    """Mixin con validaciones específicas para productos"""
    
    @field_validator('cod_producto')
    @classmethod
    def validate_cod_producto(cls, v):
        """Valida formato de código de producto"""
        if len(v) < 1:
            raise ValueError('El código de producto debe tener al menos 1 caracteres')
        return v.upper()

    @field_validator('precio')
    @classmethod
    def validate_precio(cls, v):
        """Valida que el precio sea positivo"""
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class VentaValidators:
    """Mixin con validaciones específicas para ventas"""
    
    @field_validator('tipo')
    @classmethod
    def validate_tipo(cls, v):
        """Valida tipo de venta"""
        if v not in ['credito', 'de_contado']:
            raise ValueError('El tipo debe ser "credito" o "de_contado"')
        return v

    @field_validator('monto_total_bs')
    @classmethod
    def validate_monto(cls, v):
        """Valida que el monto sea positivo"""
        if v <= 0:
            raise ValueError('El monto debe ser mayor a 0')
        return v