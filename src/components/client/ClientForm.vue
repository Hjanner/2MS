<script setup>
import { ref, watch  } from 'vue';

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
  }
});

const emit = defineEmits(['submit', 'update:show']);

const client = ref({
    ci_cliente: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
});

// Actualizar el formulario cuando cambia clientData
watch(() => props.clientData, (newVal) => {
  if (newVal) {
    client.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

function resetForm() {
  client.value = {
    ci_cliente: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
  };
}

function close() {
  emit('update:show', false);
}

function handleSubmit() {
  if (!client.value.nombre || !client.value.ci_cliente) return;
  resetForm();
  emit('submit', client.value);
}
</script>

<template>
    <v-dialog :model-value="show" 
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
              class="mb-4"
            />
            <v-text-field
              v-model="client.ci_cliente"
              label="Ingresar CI"
              type="number"
              required
              :rules="[
                v => !!v || 'CI es requerido',
                v => /^\d+$/.test(v) || 'CI debe ser un número',
              ]"
            />
            <v-text-field
              v-model="client.tlf"
              label="Ingresar teléfono"
              type="number"
              required
              :rules="[
                v => !!v || 'Teléfono es requerido',
                v => /^\d+$/.test(v) || 'Teléfono debe ser un número',
              ]"
            />
            <v-text-field
              v-model="client.depto_escuela"
              label="Ingresar departamento"
              required
              :rules="[
                v => !!v || 'Departamento es requerido',
              ]"
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
  
