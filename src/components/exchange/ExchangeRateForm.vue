<script setup>
import { ref, watch, computed } from 'vue';
import BaseFormDialog from '@/components/forms/BaseFormDialog.vue';
import { validateRequired, validatePrice } from '@/utils/validators.js';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar Tasa de Cambio Manual'
  },
  loading: Boolean,
  errors: { 
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['submit', 'update:show', 'update:errors']);

const exchangeRate = ref({
  fecha: '',
  valor_usd_bs: '',
  origen: 'Manual'
});

const localErrors = ref({});

// Reglas de validación usando los validadores importados
const fechaRules = [
  validateRequired('Fecha y hora'),
  v => {
    const date = new Date(v);
    const now = new Date();
    return date <= now || 'La fecha no puede ser futura';
  }
];

const valorRules = [
  validateRequired('Valor USD/BS'),
  v => {
    const num = parseFloat(v);
    if (isNaN(num)) return 'Debe ser un número válido';
    if (num <= 0) return 'El valor debe ser mayor a 0';
    if (num < 0.01) return 'El valor debe ser mayor a 0.01';
    if (num > 1000000) return 'El valor parece demasiado alto';
    return true;
  }
];

// Manejo de errores
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true });

// Inicializar fecha actual cuando se abre el formulario
watch(() => props.show, (newVal) => {
  if (newVal) {
    resetForm();
  }
}, { immediate: true });

function handleSubmit() {
  localErrors.value = {};
  emit('update:errors', {});
  
  // Validación básica antes de enviar
  if (!exchangeRate.value.fecha || !exchangeRate.value.valor_usd_bs) {
    localErrors.value.general = 'Complete todos los campos requeridos';
    return;
  }

  // Preparar datos para enviar
  const exchangeRateData = {
    fecha: exchangeRate.value.fecha,
    valor_usd_bs: parseFloat(exchangeRate.value.valor_usd_bs),
    origen: 'Manual'
  };

  emit('submit', exchangeRateData);
}

function resetForm() {
  // Establecer fecha y hora actual
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  
  exchangeRate.value = {
    fecha: `${year}-${month}-${day}T${hours}:${minutes}`,
    valor_usd_bs: '',
    origen: 'Manual'
  };
}

function close() {
  emit('update:show', false);
  localErrors.value = {};
}

// Formatear el valor para mostrar
const formattedValue = computed(() => {
  if (!exchangeRate.value.valor_usd_bs) return '';
  const num = parseFloat(exchangeRate.value.valor_usd_bs);
  if (isNaN(num)) return exchangeRate.value.valor_usd_bs;
  return new Intl.NumberFormat('es-VE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 4
  }).format(num);
});
</script>

<template>
  <BaseFormDialog
    :show="show"
    :title="title"
    :loading="loading"
    mode="add"
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

    <!-- Información sobre tasa manual -->
    <v-alert
      type="info"
      variant="tonal"
      class="mb-4"
    >
      <template #prepend>
        <v-icon>mdi-account-edit</v-icon>
      </template>
      <strong>Tasa Manual:</strong> Esta tasa será registrada con origen "Manual" y la fecha/hora que especifique.
    </v-alert>

    <!-- Campo fecha y hora -->
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="exchangeRate.fecha"
          label="Fecha y Hora *"
          type="datetime-local"
          variant="outlined"
          :rules="fechaRules"
          :error-messages="localErrors.fecha"
          prepend-inner-icon="mdi-calendar-clock"
          hint="Seleccione la fecha y hora de la tasa de cambio"
        />
      </v-col>
    </v-row>

    <!-- Campo valor USD/BS -->
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="exchangeRate.valor_usd_bs"
          label="Valor 1 USD en Bolívares *"
          variant="outlined"
          type="number"
          step="0.0001"
          min="0.01"
          max="1000000"
          :rules="valorRules"
          :error-messages="localErrors.valor_usd_bs"
          prepend-inner-icon="mdi-currency-usd"
          suffix="BS"
          placeholder="36.5000"
          hint="Ingrese el valor de 1 dólar estadounidense en bolívares"
        />
      </v-col>
    </v-row>

    <!-- Vista previa del valor formateado -->
    <v-card
      v-if="exchangeRate.valor_usd_bs && !isNaN(parseFloat(exchangeRate.valor_usd_bs))"
      variant="tonal"
      color="success"
      class="mt-4"
    >
      <v-card-text class="d-flex align-center justify-center">
        <div class="text-center">
          <div class="text-h5 font-weight-bold">
            <v-icon class="me-2">mdi-currency-usd</v-icon>
            1 USD = {{ formattedValue }} BS
          </div>
          <div class="text-subtitle-2 text-medium-emphasis mt-1">
            Vista previa de la tasa de cambio
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Campo origen (fijo como Manual) -->
    <v-row class="mt-2">
      <v-col cols="12">
        <v-text-field
          v-model="exchangeRate.origen"
          label="Origen"
          variant="outlined"
          readonly
          prepend-inner-icon="mdi-account-edit"
          hint="Las tasas creadas desde esta interfaz siempre son de origen Manual"
        >
          <template #append-inner>
            <v-chip
              color="primary"
              variant="tonal"
              size="small"
            >
              <v-icon start>mdi-account-edit</v-icon>
              Manual
            </v-chip>
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <!-- Consejos para la tasa -->
    <v-expansion-panels 
      variant="accordion"
      class="mt-4"
    >
      <v-expansion-panel title="Consejos para registrar tasas">
        <v-expansion-panel-text>
          <v-list density="compact">
            <v-list-item>
              <template #prepend>
                <v-icon color="info">mdi-lightbulb-outline</v-icon>
              </template>
              <v-list-item-title>
                Verifique que la tasa sea actual y confiable
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon color="info">mdi-clock-outline</v-icon>
              </template>
              <v-list-item-title>
                Use la fecha y hora exacta de cuando obtuvo la tasa
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon color="info">mdi-decimal</v-icon>
              </template>
              <v-list-item-title>
                Incluya hasta 4 decimales para mayor precisión
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </BaseFormDialog>
</template>