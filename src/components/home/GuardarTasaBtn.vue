<template>
  <v-btn 
    color="primary"
    icon="mdi-currency-usd" 
    variant="tonal" 
    size="small"
    class="ml-4"
    @click="guardarTasa" 
    />
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { useFetch } from '@/composables/useFetch.js'
import { useSnackbar } from '@/composables/useSnackbar.js'

const loading = ref(false)
const { showSnackbar } = useSnackbar()
const emit = defineEmits(['tasa-guardada'])

const guardarTasa = async () => {
  loading.value = true
  try {
    await useFetch('http://127.0.0.1:8000/dolar/guardar', { method: 'POST' })
    showSnackbar('Tasa guardada exitosamente', 'success')
  } catch (e) {
    showSnackbar('Error al guardar la tasa', 'error')
  } finally {
    emit('tasa-guardada')
    loading.value = false
  }
}
</script>
