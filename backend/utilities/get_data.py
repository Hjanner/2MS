# Función auxiliar para obtener datos del formulario
from typing import List

from fastapi import Depends


def get_form_data_as_dict(
    all_params: dict = Depends(lambda: {}),
    form_data: List[tuple] = Depends(lambda: [])
) -> dict:
    """Convierte los datos del formulario en un diccionario."""
    return {**all_params, **dict(form_data)}
