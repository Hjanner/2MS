<script setup>
import { ref, watch, computed } from 'vue';
import BaseFormDialog from '@/components/forms/BaseFormDialog.vue';
import {
  validateRequired,
  validateRIF,
  validatePhone,
} from '@/utils/validators';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar Proveedor'
  },
  loading: Boolean,
  supplierData: {
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

const supplier = ref({
  Rif: '',
  razon_social: '',
  direccion: '',
  tfl: '',
  persona_contacto: ''
});

const localErrors = ref({});
const isEditing = computed(() => props.mode === 'edit');

// Reglas de validación usando validators.js
const rifRules = [
  validateRequired('RIF'),
  value => validateRIF(value) === true || validateRIF(value)
];

const razonSocialRules = [
  validateRequired('Razón social'),
  v => (v && v.length >= 2) || 'Razón social debe tener al menos 2 caracteres'
];

const telefonoRules = [
  v => !v || validatePhone(v) === true || validatePhone(v)
];

// Manejo de errores
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar formulario cuando cambian los datos
watch(() => props.supplierData, (newVal) => {
  if (newVal) {
    supplier.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

function handleSubmit() {
  localErrors.value = {};
  emit('update:errors', {});
  
  // Validación básica antes de enviar
  if (!supplier.value.Rif || !supplier.value.razon_social) {
    localErrors.value.general = 'Complete los campos requeridos';
    return;
  }

  // Formatear RIF a mayúsculas y limpiar guiones
  if (supplier.value.Rif) {
    supplier.value.Rif = supplier.value.Rif.toUpperCase().replace(/-/g, '');
  }

  emit('submit', supplier.value);
}

function resetForm() {
  supplier.value = {
    Rif: '',
    razon_social: '',
    direccion: '',
    tfl: '',
    persona_contacto: ''
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

    <v-alert
      v-if="localErrors.general"
      type="error"
      variant="tonal"
      closable
      class="mb-4"
    >
      {{ localErrors.general }}
    </v-alert>

    <!-- Información básica del proveedor -->
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="supplier.Rif"
          label="RIF *"
          variant="outlined"
          :rules="rifRules"
          :error-messages="localErrors.Rif"
          :disabled="isEditing"
          placeholder="J-12345678-9"
          prepend-inner-icon="mdi-card-account-details-outline"
          counter="10"
          maxlength="10"
          @input="supplier.Rif = supplier.Rif.toUpperCase()"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="supplier.razon_social"
          label="Razón Social *"
          variant="outlined"
          :rules="razonSocialRules"
          :error-messages="localErrors.razon_social"
          prepend-inner-icon="mdi-domain"
          placeholder="Nombre comercial de la empresa"
        />
      </v-col>
    </v-row>

    <!-- Información de contacto -->
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="supplier.tfl"
          label="Teléfono"
          variant="outlined"
          :rules="telefonoRules"
          :error-messages="localErrors.tfl"
          prepend-inner-icon="mdi-phone-outline"
          placeholder="0212-1234567"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="supplier.persona_contacto"
          label="Persona de Contacto"
          variant="outlined"
          :error-messages="localErrors.persona_contacto"
          prepend-inner-icon="mdi-account-outline"
          placeholder="Nombre del contacto principal"
        />
      </v-col>
    </v-row>

    <!-- Dirección -->
    <v-row>
      <v-col cols="12">
        <v-textarea
          v-model="supplier.direccion"
          label="Dirección"
          variant="outlined"
          :error-messages="localErrors.direccion"
          prepend-inner-icon="mdi-map-marker-outline"
          rows="3"
          placeholder="Ingrese la dirección completa del proveedor"
        />
      </v-col>
    </v-row>

    <!-- Información adicional para modo edición -->
    <v-alert
      v-if="isEditing"
      type="info"
      variant="tonal"
      class="mt-4"
    >
      <template #prepend>
        <v-icon>mdi-information-outline</v-icon>
      </template>
      <strong>Nota:</strong> El RIF no puede ser modificado una vez creado el proveedor.
    </v-alert>
  </BaseFormDialog>
</template>