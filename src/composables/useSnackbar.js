import { ref } from 'vue';

const snackbar = ref({
    show: false,
    message: '',
    color: 'success'
  });
  
export function useSnackbar() {
  function showSnackbar(message, color = 'success') {
    snackbar.value = {
      show: true,
      message,
      color
    };
  }

  return {
    snackbar,
    showSnackbar
  };
}