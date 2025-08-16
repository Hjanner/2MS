<script setup>
import { validateRequired, validateCI } from '@/utils/validators';
import { computed } from 'vue';

const props = defineProps({
  modelValue: Object,
  errors: Object
});

const emit = defineEmits(['update:modelValue']);

const client = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const validationRules = {
  nombre: [validateRequired('Nombre')],
  ci_cliente: [
    validateRequired('Cédula'),
    v => /^\d+$/.test(v) || 'Cédula debe ser un número',
    v => (v && v.length >= 6) || 'Mínimo 6 dígitos',
    v => (v && v.length <= 9) || 'Máximo 9 dígitos'
  ]
};
</script>

<template>
  <div class="mb-6">
    <h3 class="text-h6 mb-4 d-flex align-center">
      <v-icon class="me-2">mdi-account</v-icon>
      Información Básica
    </h3>

    <v-text-field
      v-model="client.nombre"
      label="Nombre completo"
      required
      :rules="validationRules.nombre"
      :error-messages="errors.nombre"
      prepend-inner-icon="mdi-account-circle"
    />

    <v-text-field
      v-model="client.ci_cliente"
      label="Cédula de identidad"
      type="number"
      required
      :rules="validationRules.ci_cliente"
      :error-messages="errors.ci_cliente"
      prepend-inner-icon="mdi-card-account-details"
      class="mt-4"
    />
  </div>
</template>