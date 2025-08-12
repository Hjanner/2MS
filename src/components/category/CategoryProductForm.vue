<script setup>
import { ref, watch, computed } from 'vue';
import BaseFormDialog from '@/components/forms/BaseFormDialog.vue';
import { validateRequired } from '@/utils/validators.js';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Agregar Categoría'
  },
  loading: Boolean,
  categoryData: {
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

const category = ref({
  descr: '',
  tipo: ''
});

const localErrors = ref({});
const isEditing = computed(() => props.mode === 'edit');

// Opciones para el tipo de categoría
const tipoOptions = [
  { 
    value: 'preparado', 
    title: 'Preparado',
    subtitle: 'Productos que requieren preparación',
    icon: 'mdi-chef-hat',
    color: 'success'
  },
  { 
    value: 'noPreparado', 
    title: 'No Preparado',
    subtitle: 'Productos listos para consumo',
    icon: 'mdi-package-variant',
    color: 'warning'
  }
];

// Reglas de validación usando los validadores importados
const descrRules = [
  validateRequired('Descripción'),
  v => (v && v.length >= 3) || 'La descripción debe tener al menos 3 caracteres',
  v => (v && v.length <= 100) || 'La descripción debe tener máximo 100 caracteres'
];

const tipoRules = [
  validateRequired('Tipo de categoría'),
  v => ['preparado', 'noPreparado'].includes(v) || 'Tipo de categoría inválido'
];

// Manejo de errores
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar formulario cuando cambian los datos
watch(() => props.categoryData, (newVal) => {
  if (newVal) {
    category.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });

function handleSubmit() {
  localErrors.value = {};
  emit('update:errors', {});
  
  // Validación básica antes de enviar
  if (!category.value.descr || !category.value.tipo) {
    localErrors.value.general = 'Complete todos los campos requeridos';
    return;
  }

  // Limpiar espacios en blanco
  const cleanCategory = {
    ...category.value,
    descr: category.value.descr.trim()
  };

  emit('submit', cleanCategory);
}

function resetForm() {
  category.value = {
    descr: '',
    tipo: ''
  };
}

function close() {
  emit('update:show', false);
  localErrors.value = {};
}

// Obtener información del tipo seleccionado
const selectedTypeInfo = computed(() => {
  return tipoOptions.find(option => option.value === category.value.tipo) || null;
});
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

    <!-- Información de la categoría existente -->
    <v-alert
      v-if="isEditing && category.id_categoria"
      type="info"
      variant="tonal"
      class="mb-4"
    >
      <template #prepend>
        <v-icon>mdi-information-outline</v-icon>
      </template>
      <strong>Editando categoría ID:</strong> #{{ category.id_categoria }}
    </v-alert>

    <!-- Campo descripción -->
    <v-row>
      <v-col cols="12">
        <v-text-field
          v-model="category.descr"
          label="Descripción *"
          variant="outlined"
          :rules="descrRules"
          :error-messages="localErrors.descr"
          prepend-inner-icon="mdi-text-box-outline"
          placeholder="Ingrese la descripción de la categoría"
          counter="100"
          maxlength="100"
          clearable
        />
      </v-col>
    </v-row>

    <!-- Campo tipo -->
    <v-row>
      <v-col cols="12">
        <v-select
          v-model="category.tipo"
          label="Tipo de Categoría *"
          variant="outlined"
          :items="tipoOptions"
          item-title="title"
          item-value="value"
          :rules="tipoRules"
          :error-messages="localErrors.tipo"
          prepend-inner-icon="mdi-shape-outline"
          placeholder="Seleccione el tipo de categoría"
        >
          <template #item="{ props, item }">
            <v-list-item v-bind="props">
              <template #prepend>
                <v-icon 
                  :color="item.raw.color"
                  class="me-3"
                >
                  {{ item.raw.icon }}
                </v-icon>
              </template>
              <v-list-item-title>{{ item.raw.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.raw.subtitle }}</v-list-item-subtitle>
            </v-list-item>
          </template>

          <template #selection="{ item }">
            <v-chip
              :color="item.raw.color"
              variant="tonal"
              size="small"
            >
              <v-icon start>{{ item.raw.icon }}</v-icon>
              {{ item.raw.title }}
            </v-chip>
          </template>
        </v-select>
      </v-col>
    </v-row>

    <!-- Vista previa del tipo seleccionado -->
    <v-card
      v-if="selectedTypeInfo"
      variant="tonal"
      :color="selectedTypeInfo.color"
      class="mt-4"
    >
      <v-card-text class="d-flex align-center">
        <v-icon 
          :color="selectedTypeInfo.color"
          size="large"
          class="me-4"
        >
          {{ selectedTypeInfo.icon }}
        </v-icon>
        <div>
          <div class="text-h6">{{ selectedTypeInfo.title }}</div>
          <div class="text-subtitle-2 text-medium-emphasis">
            {{ selectedTypeInfo.subtitle }}
          </div>
        </div>
      </v-card-text>
    </v-card>

    <!-- Información sobre los tipos -->
    <v-expansion-panels 
      v-if="!isEditing"
      variant="accordion"
      class="mt-4"
    >
      <v-expansion-panel title="¿Qué significan los tipos de categoría?">
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-card variant="outlined" color="success">
                <v-card-title class="d-flex align-center">
                  <v-icon color="success" class="me-2">mdi-chef-hat</v-icon>
                  Preparado
                </v-card-title>
                <v-card-text>
                  Productos que requieren algún tipo de preparación antes de ser consumidos.
                  <br><strong>Ejemplos:</strong> Platos calientes, bebidas que se preparan, postres elaborados.
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card variant="outlined" color="warning">
                <v-card-title class="d-flex align-center">
                  <v-icon color="warning" class="me-2">mdi-package-variant</v-icon>
                  No Preparado
                </v-card-title>
                <v-card-text>
                  Productos listos para el consumo inmediato, sin necesidad de preparación.
                  <br><strong>Ejemplos:</strong> Bebidas embotelladas, snacks, productos envasados.
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </BaseFormDialog>
</template>