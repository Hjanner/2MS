<script setup>
import { ref, watch, computed } from 'vue';
import { DEPARTAMENTOS } from '@/api/data';
import BaseFormDialog from '@/components/forms/BaseFormDialog.vue';
import ClientBasicInfo from '@/components/forms/ClientBasicInfo.vue';
import ClientContactInfo from '@/components/forms/ClientContactInfo.vue';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar Cliente'
  },
  loading: Boolean,
  clientData: {
    type: Object,
    default: null
  },
  errors: { 
    type: Object,
    default: () => ({})
  },
  mode: {
    type: String,
    default: 'add',
    validator: value => ['add', 'edit'].includes(value)
  }
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

// Manejo de errores
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar formulario cuando cambian los datos
watch(() => props.clientData, (newVal) => {
  if (newVal) {
    client.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

function handleSubmit() {
  localErrors.value = {};
  emit('update:errors', {});
  
  // Validación básica antes de enviar
  if (!client.value.nombre || !client.value.ci_cliente) {
    localErrors.value.general = 'Complete los campos requeridos';
    return;
  }

  emit('submit', client.value);
}

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
  localErrors.value = {};
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