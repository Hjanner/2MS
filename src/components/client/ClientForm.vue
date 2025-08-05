<script setup>
import { ref, watch, computed } from 'vue';
import { DEPARTAMENTOS } from '@/api/data';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar un Cliente'
  },
  loading: Boolean,
  clientData: {
    type: Object,
    default: null
  },
  errors: { 
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['submit', 'update:show', 'update:errors']);

const client = ref({
  ci_cliente: '',
  nombre: '',
  tlf: '',
  depto_escuela: ''
});

const localErrors = ref({});        // Estado para los errores de la API
const searchQuery = ref('');      // Variable para la busqueda

//manejo de errores desde la api
watch(() => props.errors, (newErrors) => {
    localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar el formulario cuando cambia clientData
watch(() => props.clientData, (newVal) => {
  if (newVal) {
    client.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

// Filtrar departamentos basado en la búsqueda
const filteredDepartamentos = computed(() => {
  if (!searchQuery.value) return DEPARTAMENTOS;
  
  const query = searchQuery.value.toLowerCase();
  return DEPARTAMENTOS.filter(depto => 
    depto.toLowerCase().includes(query)
  );
});

function handleSubmit() {
  if (!client.value.nombre || !client.value.ci_cliente) return;

  localErrors.value = {};         //limpiar errroes antes de enviar
  emit('update:errors', {});

  emit('submit', client.value);
    // .then((apiErrors) => {
    //   if (apiErrors) {
    //     localErrors.value = apiErrors;
    //     emit('update:errors', apiErrors);
    //   } 
    // });

  resetForm();  
}

function resetForm() {
  client.value = {
    ci_cliente: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
  };
  searchQuery.value = '';
}

function close() {
  emit('update:show', false);
  localErrors.value = {};
}
</script>

<template>
  <v-dialog 
    :model-value="show" 
    @update:model-value="$emit('update:show', $event)"  
    max-width="500"
  >
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="client.nombre"
            label="Ingresar nombre"
            required
            :rules="[v => !!v || 'Nombre es requerido']"
            :error-messages="localErrors.nombre"
            class="mb-4"
          />
          <v-text-field
            v-model="client.ci_cliente"
            label="Ingresar CI"
            type="number"
            :rules="[
              v => !!v || 'CI es requerido',
              v => /^\d+$/.test(v) || 'CI debe ser un número',
              v => (v && v.length >= 6) || 'CI debe tener al menos 6 dígitos',
              v => (v && v.length <= 9) || 'CI debe tener 9 dígitos como máximo'
            ]"
            :error-messages="localErrors.ci_cliente"
          />
          <v-text-field
            v-model="client.tlf"
            label="Ingresar teléfono"
            type="number"
            :rules="[
              v => /^\d+$/.test(v) || 'Teléfono debe ser un número',
              v => (v && v.length == 11) || 'Teléfono debe tener 11 dígitos', 
            ]"
            :error-messages="localErrors.tlf"
          />
          
          <!-- Select con buscador -->
          <v-autocomplete
            v-model="client.depto_escuela"
            v-model:search="searchQuery"
            :items="filteredDepartamentos"
            label="Seleccionar departamento"
            clearable
            :menu-props="{ maxHeight: '200px' }"
            :error-messages="localErrors.depto_escuela"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="primary" 
          @click="close"
        >
          Cancelar
        </v-btn>

        <v-btn 
          color="primary" 
          @click="handleSubmit"
          :loading="loading"
        >
          Guardar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>