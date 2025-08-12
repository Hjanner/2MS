import { useSnackbar } from './useSnackbar';

export function useApiErrorHandler() {
  const { showSnackbar } = useSnackbar();

  /**
   * Maneja errores de API y muestra notificaciones al usuario
   * @param {Error} error - Objeto de error de la API
   * @param {Ref<Object>} [errorsRef] - Referencia reactiva para almacenar errores de validación
   * @returns {Object} - Objeto con errores parseados
   */
  const handleApiError = (error, errorsRef = null) => {
    console.error('API Error:', error);
    
    const backendErrors = {};
    let userMessage = 'Ocurrió un error inesperado';

    if (error.response) {
      // Error con respuesta del servidor
      if (error.response?.data?.detail) {
        const errorDetail = error.response.data.detail;

        if (Array.isArray(errorDetail)) {
          // Errores de validación (Pydantic)
          errorDetail.forEach(err => {
            if (err.loc && err.loc.length > 1) {
              const field = err.loc[1];
              backendErrors[field] = err.msg;
            }
          });
          userMessage = 'Error de validación: ' + Object.values(backendErrors).join(', ');
        } else if (typeof errorDetail === 'object' && errorDetail.field) {
          // Error estructurado
          backendErrors[errorDetail.field] = errorDetail.message;
          userMessage = errorDetail.message;
        } else if (typeof errorDetail === 'string') {
          // Mensaje directo
          backendErrors.general = errorDetail;
          userMessage = errorDetail;
        }
      } else {
        // Error HTTP estándar
        userMessage = error.response.data?.message || 
                     `Error del servidor (${error.response.status})`;
      }
    } else if (error.request) {
      // Error de red (sin respuesta)
      userMessage = 'Error de conexión con el servidor';
      console.error('Network Error:', error.request);
    } else {
      // Error en configuración de la petición
      userMessage = `Error: ${error.message}`;
    }

    // Asignar errores a la referencia si se proporcionó
    if (errorsRef) {
      errorsRef.value = backendErrors;
    }

    // Mostrar notificación al usuario
    showSnackbar(userMessage, 'error');

    return backendErrors;
  };

  /**
   * Maneja éxito de operaciones y muestra notificación
   * @param {string} message - Mensaje a mostrar
   * @param {string} [action] - Acción realizada (para mensaje genérico)
   */
  const handleSuccess = (message, action = 'operación') => {
    const successMessage = message || `${action} realizada exitosamente`;
    showSnackbar(successMessage, 'success');
  };

  return {
    handleApiError,
    handleSuccess
  };
}