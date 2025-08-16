<script setup>
import { ref, watch, computed } from 'vue';
import { DEPARTAMENTOS } from '@/api/data';
import BaseFormDialog from '@/components/forms/BaseFormDialog.vue';
import ClientBasicInfo from '@/components/forms/ClientBasicInfo.vue';
import ClientContactInfo from '@/components/forms/ClientContactInfo.vue';

const props = defineProps({
  show: Boolean,
  title: String,
  loading: Boolean,
  clientData: Object,
  errors: Object,
  mode: String
});

const emit = defineEmits(['submit', 'update:show', 'update:errors']);

const client = ref({
  ci_cliente: '',
  nombre: '',
  tlf: '',
  depto_escuela: ''
});

const localErrors = ref({});
const isEditing = computed(() => props.mode === 'edit');

// Sincronización de errores
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true, deep: true });

// Sincronización de datos
watch(() => props.clientData, (newVal) => {
  client.value = newVal ? { ...newVal } : resetForm();
}, { immediate: true });

function handleSubmit() {
  localErrors.value = {};
  emit('update:errors', {});
  
  // Validación básica del frontend
  if (!client.value.nombre) {
    localErrors.value.nombre = 'El nombre es requerido';
  }
  if (!client.value.ci_cliente) {
    localErrors.value.ci_cliente = 'La cédula es requerida';
  }

  if (Object.keys(localErrors.value).length > 0) {
    return;
  }

  emit('submit', client.value);
}

function resetForm() {
  return {
    ci_cliente: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
  };
}

function close() {
  emit('update:show', false);
  emit('update:errors', {});
}
</script>

<template>
  <BaseFormDialog
    :show="show"
    :title="title"
    :loading="loading"
    :mode="mode"
    @update:show="$emit('update:show', $event)"
    @submit="handleSubmit"
  >
    <template #title-append>
      <v-chip
        v-if="isEditing"
        color="primary"
        variant="tonal"
        size="small"
      >
        <v-icon start>mdi-pencil</v-icon>
        Editando
      </v-chip>
    </template>

    <v-alert
      v-if="localErrors.general"
      type="error"
      variant="tonal"
      closable
      class="mb-4"
    >
      {{ localErrors.general }}
    </v-alert>

    <ClientBasicInfo
      v-model="client"
      :errors="localErrors"
    />

    <ClientContactInfo
      v-model="client"
      :errors="localErrors"
      :departamentos="DEPARTAMENTOS"
    />
  </BaseFormDialog>
</template>