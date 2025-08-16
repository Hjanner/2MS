#contiene validaciones comunes
def validate_only_digits(value: str, field_name: str) -> str:
    if not value.isdigit():
        raise ValueError(f"{field_name} debe contener solo números")
    return value

def validate_max_length(value: str, max_len: int, field_name: str) -> str:
    if len(value) > max_len:
        raise ValueError(f"{field_name} no puede tener más de {max_len} caracteres")
    return value

def validate_phone(value: str, field_name: str = "Teléfono") -> str:
    if not value.isdigit() or len(value) != 11:
        raise ValueError(f"{field_name} debe tener exactamente 11 dígitos numéricos")
    return value

def validate_name(value: str, field_name: str = "Nombre") -> str:
    if any(char.isdigit() for char in value):
        raise ValueError(f"{field_name} no puede contener números")
    return value.title()

def validate_rif(value: str) -> str:
    if not value.startswith(('V', 'E', 'J', 'P', 'G')):
        raise ValueError('El RIF debe comenzar con V, E, J, P o G')
    if len(value) < 9:
        raise ValueError('El RIF debe tener al menos 9 caracteres')
    return value.upper()

def validate_starts_with(value: str, prefixes: list, field_name: str) -> str:
    if not any(value.startswith(p) for p in prefixes):
        raise ValueError(f"{field_name} debe comenzar con {' o '.join(prefixes)}")
    return value

def validate_positive_number(value: float, field_name: str) -> float:
    if value <= 0:
        raise ValueError(f"{field_name} debe ser mayor a 0")
    return value

def validate_non_negative_number(value: float, field_name: str) -> float:
    if value < 0:
        raise ValueError(f"{field_name} no puede ser negativo")
    return value

def validate_enum(value: str, allowed: list, field_name: str) -> str:
    if value not in allowed:
        raise ValueError(f"{field_name} debe ser uno de {allowed}")
    return value

def validate_not_empty(value: str, field_name: str) -> str:
    if len(value.strip()) == 0:
        raise ValueError(f"{field_name} no puede estar vacío")
    return value
