<script setup>
import { validateMinQuantity, validateCost, validateRIF, validatePositiveNumber } from '@/utils/validators.js';

const props = defineProps({
  modelValue: Object,
  errors: Object,
  unidadesMedida: {
    type: Array,
    default: () => ['unidad', 'kg', 'g', 'ml', 'l']
  }
});

const emit = defineEmits(['update:modelValue']);

const inventoryData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const validationRules = {
  cant_min: [validateMinQuantity],
  cant_actual: [validatePositiveNumber('Cantidad actual')],
  costo_compra: [validateCost],
  unidad_medida: [(v) => !!v || 'Unidad de medida es requerida'],
  Rif: [validateRIF]
};
</script>

<template>
  <div class="mb-6">
    <h3 class="text-h6 mb-4 d-flex align-center">
      <v-icon class="me-2" color="blue">mdi-package-variant</v-icon>
      Información de Inventario
    </h3>

    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="inventoryData.cant_min"
          label="Cantidad mínima"
          type="number"
          min="0"
          required
          :rules="validationRules.cant_min"
          :error-messages="errors.cant_min"
          hint="Stock mínimo requerido"
          persistent-hint
          prepend-inner-icon="mdi-alert"
        />
      </v-col>

      <v-col cols="12" md="4">
        <v-text-field
          v-model="inventoryData.cant_actual"
          label="Cantidad actual"
          type="number"
          min="0"
          :rules="validationRules.cant_actual"
          :error-messages="errors.cant_actual"
          hint="Stock actual disponible"
          persistent-hint
          prepend-inner-icon="mdi-package"
        />
      </v-col>

      <v-col cols="12" md="4">
        <v-select
          v-model="inventoryData.unidad_medida"
          :items="unidadesMedida"
          label="Unidad de medida"
          required
          :error-messages="errors.unidad_medida"
          hint="Unidad de medida del producto"
          persistent-hint
          prepend-inner-icon="mdi-ruler"
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="inventoryData.costo_compra"
          label="Costo de compra"
          type="number"
          step="0.01"
          min="0"
          required
          :rules="validationRules.costo_compra"
          :error-messages="errors.costo_compra"
          prefix="$"
          hint="Costo unitario de compra"
          persistent-hint
          prepend-inner-icon="mdi-cash"
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field
          v-model="inventoryData.Rif"
          label="RIF del Proveedor"
          :error-messages="errors.Rif"
          hint="RIF del proveedor (opcional)"
          persistent-hint
          prepend-inner-icon="mdi-account-tie"
          placeholder="J-12345678-9"
        />
      </v-col>
    </v-row>
  </div>
</template>