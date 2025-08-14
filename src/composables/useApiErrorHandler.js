import { useSnackbar } from './useSnackbar';

export function useApiErrorHandler() {
  const { showSnackbar } = useSnackbar();

  /**
   * Maneja errores de API de manera unificada
   * @param {Error} error - Objeto de error
   * @param {Ref<Object>} [errorsRef] - Referencia reactiva para errores de formulario
   * @returns {Object} - Objeto con errores estructurados
   */
  const handleApiError = (error, errorsRef = null) => {
    console.error('API Error:', error);
    const backendErrors = {};
    let userMessage = 'Ocurrió un error inesperado';

    if (error.response) {
      const responseData = error.response.data;
      
      // Caso 1: Error estructurado con detail
      if (responseData.detail) {
        const detail = responseData.detail;

        // 1a: Error de duplicado (formato específico)
        if (detail.code === 'DUPLICATE_KEY') {
          backendErrors[detail.field] = detail.message;
          userMessage = `${detail.message} (Valor: ${detail.value})`;
        }
        // 1b: Lista de errores de validación (Pydantic)
        else if (Array.isArray(detail)) {
          detail.forEach(err => {
            if (err.loc?.length > 1) {
              const field = err.loc[1];
              backendErrors[field] = err.msg;
            }
          });
          userMessage = 'Revise los campos marcados';
        }
        // 1c: Error de campo específico
        else if (typeof detail === 'object' && detail.field) {
          backendErrors[detail.field] = detail.message;
          userMessage = detail.message;
        }
        // 1d: Mensaje directo
        else {
          userMessage = typeof detail === 'string' ? detail : detail.message;
          backendErrors.general = userMessage;
        }
      }
      // Caso 2: Error con mensaje directo
      else if (responseData.message) {
        userMessage = responseData.message;
        backendErrors.general = userMessage;
      }
      // Caso 3: Error HTTP estándar
      else {
        userMessage = `Error del servidor (${error.response.status})`;
        backendErrors.general = userMessage;
      }
    } 
    // Error de red
    else if (error.request) {
      userMessage = 'Error de conexión con el servidor';
      backendErrors.general = userMessage;
    } 
    // Error de configuración
    else {
      userMessage = `Error: ${error.message}`;
      backendErrors.general = userMessage;
    }

    // Asignar errores a la referencia reactiva si existe
    if (errorsRef) {
      errorsRef.value = backendErrors;
    }

    showSnackbar(userMessage, 'error');
    return backendErrors;
  };

  /**
   * Maneja éxito de operaciones
   * @param {string} message - Mensaje personalizado
   * @param {string} [action] - Acción genérica (para mensaje por defecto)
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