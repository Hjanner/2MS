<script setup>
import { ref, watch } from 'vue';
import { DEPARTAMENTOS } from '@/api/data';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar un Producto'
  },
  loading: Boolean,
  productData: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['submit', 'update:show']);

const product = ref({
  ci_producto: '',
  nombre: '',
  tlf: '',
  depto_escuela: ''
});

// Actualizar el formulario cuando cambia productData
watch(() => props.productData, (newVal) => {
  if (newVal) {
    product.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

function resetForm() {
  product.value = {
    ci_producto: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
  };
}


function close() {
  emit('update:show', false);
}

function handleSubmit() {
  if (!product.value.nombre || !product.value.ci_producto) return;
  resetForm();
  emit('submit', product.value);
}

// Variable para la busqueda
const search = ref(null);

// Función para filtrar las opciones
function customFilter(item, queryText) {
  const normalizedQuery = queryText.toLowerCase();
  const normalizedItemText = item.value.toLowerCase();
  
  return normalizedItemText.includes(normalizedQuery);
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
            v-model="product.nombre"
            label="Ingresar nombre"
            required
            :rules="[v => !!v || 'Nombre es requerido']"
            class="mb-4"
          />
          <v-text-field
            v-model="product.ci_producto"
            label="Ingresar CI"
            type="number"
            required
            :rules="[
              v => !!v || 'CI es requerido',
              v => /^\d+$/.test(v) || 'CI debe ser un número',
            ]"
          />
          <v-text-field
            v-model="product.tlf"
            label="Ingresar teléfono"
            type="number"
            :rules="[
              v => /^\d+$/.test(v) || 'Teléfono debe ser un número',
            ]"
          />
          <v-select
            v-model="product.depto_escuela"
            :items="DEPARTAMENTOS"
            label="Seleccionar departamento"
            required
            v-model:search="search"
            :custom-filter="customFilter"
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