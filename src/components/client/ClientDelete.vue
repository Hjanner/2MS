<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  clientData: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['update:show', 'confirmDelete']);

function closeDialog() {
  emit('update:show', false);
}

function handleConfirm() {    
  if (props.clientData) {
    emit('confirmDelete', props.clientData.ci_cliente);
  }
}
</script>

<template>
  <v-dialog :model-value="show" max-width="500" persistent>
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon color="error" class="mr-2">mdi-alert-circle</v-icon>
        Confirmar Eliminación
      </v-card-title>
      <v-progress-linear
        v-if="loading"
        indeterminate
        color="primary"
        class="mb-4"
      ></v-progress-linear> 
      <v-card-text>
        <div v-if="clientData">
          <p class="mb-4">
            ¿Estás seguro de que deseas eliminar al cliente
            <strong>{{ clientData.nombre }}</strong>?
          </p>
          <p class="text-caption text-medium-emphasis">
            Esta acción no se puede deshacer.
          </p>
        </div>
        <div v-else>
          <p class="mb-4">¿Estás seguro de que deseas eliminar este cliente?</p>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="closeDialog"
          :disabled="loading"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="error"
          @click="handleConfirm"
          :loading="loading"
        >
          Eliminar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
