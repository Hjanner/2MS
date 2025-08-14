<script setup>
import { ref, computed, watch } from 'vue';
import { TIPO_MOVIMIENTO_OPTIONS, REFERENCIA_OPTIONS } from '@/api/data';
import { getCurrentDate } from '@/utils/formatters'
import BaseForm from '@/components/forms/BaseFormDialog.vue';

const props = defineProps({
  show: Boolean,
  loading: Boolean,
  productData: Object,
  errors: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['update:show', 'submit']);

// Datos del formulario
const formData = ref({
  tipo_movimiento: '',
  referencia: '',
  cant_movida: null,
  costo_unitario: null,
  comentario: '',
  fc_actualizacion: getCurrentDate()
});

// Vista previa del resultado del ajuste
const previewResult = computed(() => {
  if (!formData.value.tipo_movimiento || !formData.value.cant_movida || !props.productData) {
    return { message: '', newStock: 0, type: 'info' };
  }

  const currentStock = props.productData.cant_actual;
  const cantidad = formData.value.cant_movida;
  const isEntrada = formData.value.tipo_movimiento === 'entrada';
  
  const newStock = isEntrada ? currentStock + cantidad : currentStock - cantidad;
  
  let message = '';
  let type = 'info';
  
  if (isEntrada) {
    message = `Se añadirán ${cantidad} ${props.productData.unidad_medida} al inventario`;
    type = 'success';
  } else {
    message = `Se reducirán ${cantidad} ${props.productData.unidad_medida} del inventario`;
    type = newStock < 0 ? 'error' : 'warning';
    
    if (newStock < 0) {
      message += ` (¡ATENCIÓN: Stock quedaría negativo!)`;
    } else if (newStock < props.productData.cant_min) {
      message += ` (Stock por debajo del mínimo)`;
      type = 'warning';
    }
  }
  
  return { message, newStock: Math.max(0, newStock), type };
});

// Manejar envío del formulario
function handleSubmit() {
  if (!validateForm()) return;
  
  const movimientoData = {
    cod_producto: props.productData.cod_producto,
    referencia: formData.value.tipo_movimiento === 'entrada' ? 'ajuste' : formData.value.referencia,
    tipo_movimiento: formData.value.tipo_movimiento,
    cant_movida: formData.value.cant_movida,
    comentario: formData.value.comentario || null,
    costo_unitario: formData.value.costo_unitario || null,
    fc_actualizacion: formData.value.fc_actualizacion,
    id_compra: null
  };
  
  emit('submit', movimientoData);
}

// Validación básica del formulario
function validateForm() {
  if (!formData.value.tipo_movimiento) {
    return false;
  }
  
  // Si es salida, la referencia es obligatoria
  if (formData.value.tipo_movimiento === 'salida' && !formData.value.referencia) {
    return false;
  }
  
  if (!formData.value.cant_movida || formData.value.cant_movida <= 0) {
    return false;
  }
  
  if (!formData.value.fc_actualizacion) {
    return false;
  }
  
  return true;
}

// Resetear formulario cuando se cierre el diálogo
watch(() => props.show, (newValue) => {
  if (!newValue) {
    // Reset form when dialog closes
    formData.value = {
      tipo_movimiento: '',
      referencia: '',
      cant_movida: null,
      costo_unitario: null,
      comentario: '',
      fc_actualizacion: getCurrentDate()
    };
  }
});

// Resetear referencia cuando cambie el tipo de movimiento
watch(() => formData.value.tipo_movimiento, (newValue) => {
  if (newValue === 'entrada') {
    formData.value.referencia = '';
  }
});
</script>

<template>
  <BaseForm
    :show="show"
    :title="`Ajustar Inventario - ${productData?.nombre || ''}`"
    :loading="loading"
    :mode="'add'"
    @update:show="$emit('update:show', $event)"
    @submit="handleSubmit"
  >
    <v-container>
      <!-- Información del producto -->
      <v-row>
        <v-col cols="12">
          <v-card variant="outlined" class="mb-4">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <v-icon class="me-2" color="primary">mdi-package-variant</v-icon>
                <span class="text-h6">{{ productData?.nombre }}</span>
              </div>
              <v-chip class="me-2" size="small">{{ productData?.cod_producto }}</v-chip>
              <v-chip size="small" color="info">{{ productData?.categoria_descr }}</v-chip>
              <v-divider class="my-3"></v-divider>
              <div class="d-flex justify-space-between">
                <div>
                  <span class="text-body-2 text-medium-emphasis">Stock actual:</span>
                  <span class="text-h6 ms-2">{{ productData?.cant_actual }} {{ productData?.unidad_medida }}</span>
                </div>
                <div>
                  <span class="text-body-2 text-medium-emphasis">Stock mínimo:</span>
                  <span class="text-h6 ms-2">{{ productData?.cant_min }} {{ productData?.unidad_medida }}</span>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Formulario de ajuste -->
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.tipo_movimiento"
            :items="TIPO_MOVIMIENTO_OPTIONS"
            label="Tipo de ajuste"
            variant="outlined"
            :error-messages="errors.tipo_movimiento"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <template v-slot:prepend>
                  <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                </template>
              </v-list-item>
            </template>
            <template v-slot:selection="{ item }">
              <div class="d-flex align-center">
                <v-icon :color="item.raw.color" class="me-2">{{ item.raw.icon }}</v-icon>
                {{ item.raw.title }}
              </div>
            </template>
          </v-select>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="formData.cant_movida"
            type="number"
            label="Cantidad a ajustar"
            variant="outlined"
            :error-messages="errors.cant_movida"
            :suffix="productData?.unidad_medida"
            min="1"
            required
          />
        </v-col>
      </v-row>

      <!-- Campo de referencia para movimientos de salida -->
      <v-row v-if="formData.tipo_movimiento === 'salida'">
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.referencia"
            :items="REFERENCIA_OPTIONS"
            label="Referencia del movimiento"
            variant="outlined"
            :error-messages="errors.referencia"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <template v-slot:prepend>
                  <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                </template>
              </v-list-item>
            </template>
            <template v-slot:selection="{ item }">
              <div class="d-flex align-center">
                <v-icon :color="item.raw.color" class="me-2">{{ item.raw.icon }}</v-icon>
                {{ item.raw.title }}
              </div>
            </template>
          </v-select>
        </v-col>
        <v-col cols="12" md="6">
          <!-- Campo vacío para mantener el diseño -->
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model.number="formData.costo_unitario"
            type="number"
            label="Costo unitario (opcional)"
            variant="outlined"
            :error-messages="errors.costo_unitario"
            prefix="$"
            step="0.01"
            min="0"
          />
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.fc_actualizacion"
            type="date"
            label="Fecha del movimiento"
            variant="outlined"
            :error-messages="errors.fc_actualizacion"
            required
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <v-textarea
            v-model="formData.comentario"
            label="Comentario (opcional)"
            variant="outlined"
            :error-messages="errors.comentario"
            rows="3"
            counter="255"
            placeholder="Describe el motivo del ajuste..."
          />
        </v-col>
      </v-row>

      <!-- Vista previa del resultado -->
      <v-row v-if="formData.tipo_movimiento && formData.cant_movida">
        <v-col cols="12">
          <v-alert
            :type="previewResult.type"
            variant="tonal"
          >
            <div class="d-flex align-center justify-space-between">
              <div>
                <strong>Vista previa:</strong>
                {{ previewResult.message }}
              </div>
              <v-chip :color="previewResult.type" variant="elevated">
                {{ previewResult.newStock }} {{ productData?.unidad_medida }}
              </v-chip>
            </div>
          </v-alert>
        </v-col>
      </v-row>

      <!-- Mensaje de error general -->
      <v-row v-if="errors.general">
        <v-col cols="12">
          <v-alert type="error" variant="tonal">
            {{ errors.general }}
          </v-alert>
        </v-col>
      </v-row>
    </v-container>
  </BaseForm>
</template>
