import { useSnackbar } from '@/composables/useSnackbar';

/**
 * Composable para manejar errores de API de forma consistente en toda la aplicación.
 * Proporciona funciones para manejar errores y mostrar mensajes de éxito.
 */
export function useApiErrorHandler() {
  const { showSnackbar } = useSnackbar();

  /**
   * Maneja errores de API y los asigna a un objeto de errores de referencia si se proporciona.
   * @param {Error} error - El objeto de error capturado
   * @param {Ref<Object>} [errorRef] - Referencia opcional a un objeto de errores para asignar errores de validación
   * @param {Object} [options] - Opciones adicionales
   * @param {boolean} [options.showSnackbar=true] - Controla si se muestra el snackbar de error
   */
  function handleApiError(error, errorRef, options = { showSnackbar: true }) {
    console.log('Error de API:', error);
    const backendErrors = {};

    if (error.response) {
      if (error.response?.data?.detail) {
        const errorDetail = error.response.data.detail;

        if (Array.isArray(errorDetail)) {
          // Múltiples errores de validación (estilo FastAPI)
          errorDetail.forEach(err => {
            if (err.loc && err.loc.length > 1) {
              backendErrors[err.loc[1]] = err.msg;
            }
          });
        } else if (typeof errorDetail === 'object' && errorDetail.field) {
          // Error de campo específico
          backendErrors[errorDetail.field] = errorDetail.message;
        } else if (typeof errorDetail === 'string') {
          // Error general
          backendErrors.general = errorDetail;
        }

        // Asignar errores al reference si se proporcionó
        if (errorRef) {
          errorRef.value = backendErrors;
        }

        if (options.showSnackbar) {
          const errorMessages = Object.values(backendErrors).join(', ');
          showSnackbar(errorMessages || 'Ocurrió un error inesperado.', 'error');
        }
      } else {
        // Otros tipos de respuestas de error
        const message = error.response.data?.message || `Error del servidor: ${error.response.status}`;
        if (options.showSnackbar) {
          showSnackbar(message, 'error');
        }
      }
    } else if (error.request) {
      console.log('Error de red:', error.request);
      if (options.showSnackbar) {
        showSnackbar('Error de conexión con el servidor', 'error');
      }
    } else {
      console.log('Error:', error.message);
      if (options.showSnackbar) {
        showSnackbar('Error inesperado: ' + error.message, 'error');
      }
    }
  }

  /**
   * Muestra un mensaje de éxito en un snackbar
   * @param {string} message - Mensaje a mostrar
   */
  function handleSuccess(message) {
    showSnackbar(message, 'success');
  }

  return {
    handleApiError,
    handleSuccess
  };
}