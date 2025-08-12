<script setup>
import { validatePhone } from '@/utils/validators';
import { computed, ref } from 'vue';

const props = defineProps({
  modelValue: Object,
  errors: Object,
  departamentos: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const client = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const searchQuery = ref('');

const validationRules = {
  tlf: [validatePhone],
  depto_escuela: []
};

const filteredDepartamentos = computed(() => {
  if (!searchQuery.value) return props.departamentos;
  const query = searchQuery.value.toLowerCase();
  return props.departamentos.filter(depto => 
    depto.toLowerCase().includes(query)
  );
});
</script>

<template>
  <div class="mb-4">
    <h3 class="text-h6 mb-4 d-flex align-center">
      <v-icon class="me-2">mdi-phone</v-icon>
      Información de Contacto
    </h3>

    <v-text-field
      v-model="client.tlf"
      label="Teléfono"
      type="number"
      :rules="validationRules.tlf"
      :error-messages="errors.tlf"
      prepend-inner-icon="mdi-phone"
    />

    <v-autocomplete
      v-model="client.depto_escuela"
      v-model:search="searchQuery"
      :items="filteredDepartamentos"
      label="Departamento/Escuela"
      clearable
      :menu-props="{ maxHeight: '200px' }"
      :error-messages="errors.depto_escuela"
      prepend-inner-icon="mdi-office-building"
      class="mt-4"
    />
  </div>
</template>