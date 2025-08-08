<script setup>
import { ref, watch, computed } from 'vue';

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
  },
  categorias: {
    type: Array,
    default: () => []
  },
  errors: { 
    type: Object,
    default: () => ({})
  },
  mode: {
    type: String,
    default: 'add', // 'add' o 'edit'
    validator: value => ['add', 'edit'].includes(value)
  }
});

const emit = defineEmits(['submit', 'update:show', 'update:errors']);

// Estado del producto base
const product = ref({
  cod_producto: '',
  nombre: '',
  precio_usd: '',
  img: null,
  id_categoria: null,
  tipo_producto: 'noPreparado' // Valor por defecto
});

// Estados específicos para productos no preparados
const noPreparadoData = ref({
  cant_min: '',
  cant_actual: '',
  costo_compra: '',
  unidad_medida: 'unidad',
  Rif: ''
});

// Estados específicos para productos preparados
const preparadoData = ref({
  descr_preparado: ''
});

const localErrors = ref({});
const searchQuery = ref('');
const imagePreview = ref(null);
const fileInput = ref(null);
const isEditing = computed(() => props.mode === 'edit' || !!props.productData);

// Opciones para unidades de medida
const unidadesMedida = [
  'unidad',
  'kg',
  'gramos',
  'litros',
  'mililitros',
  'piezas',
  'metros',
  'centímetros'
];

// Determinar si el tipo de producto es preparado basado en la categoría seleccionada
const tipoProductoFromCategoria = computed(() => {
  if (!product.value.id_categoria) return 'noPreparado';
  const categoria = props.categorias.find(c => c.id_categoria === product.value.id_categoria);
  return categoria?.tipo || 'noPreparado';
});

// Actualizar tipo de producto cuando cambia la categoría
watch(() => product.value.id_categoria, () => {
  product.value.tipo_producto = tipoProductoFromCategoria.value;
});

// Manejo de errores desde la API
watch(() => props.errors, (newErrors) => {
  localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar el formulario cuando cambia productData
watch(() => props.productData, (newVal) => {
  if (newVal) {
    // Datos básicos del producto
    product.value = {
      cod_producto: newVal.cod_producto || '',
      nombre: newVal.nombre || '',
      precio_usd: newVal.precio_usd || '',
      img: newVal.img || null,
      id_categoria: newVal.id_categoria || null,
      tipo_producto: newVal.tipo_producto || 'noPreparado'
    };

    // Datos específicos según el tipo
    if (newVal.tipo_producto === 'noPreparado') {
      noPreparadoData.value = {
        cant_min: newVal.cant_min || '',
        cant_actual: newVal.cant_actual || '',
        costo_compra: newVal.costo_compra || '',
        unidad_medida: newVal.unidad_medida || 'unidad',
        Rif: newVal.Rif || ''
      };
    } else {
      preparadoData.value = {
        descr_preparado: newVal.descr_preparado || ''
      };
    }

    // Establecer preview de imagen si existe
    if (newVal.img) {
      imagePreview.value = newVal.img;
    }
  } else {
    resetForm();
  }
}, { immediate: true });

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Validar tipo de archivo
  if (!file.type.match('image.*')) {
    localErrors.value.img = 'Solo se permiten imágenes';
    return;
  }

  // Validar tamaño (máximo 2MB)
  if (file.size > 2 * 1024 * 1024) {
    localErrors.value.img = 'La imagen no debe exceder 2MB';
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    product.value.img = e.target.result;
    imagePreview.value = e.target.result;
    localErrors.value.img = null;
  };
  reader.readAsDataURL(file);
}

function removeImage() {
  imagePreview.value = null;
  product.value.img = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

// Formatear categorías para el autocomplete
const formattedCategorias = computed(() => {
  return props.categorias.map(categoria => ({
    value: categoria.id_categoria,
    text: `${categoria.descr} (${categoria.tipo})`,
    title: categoria.descr,
    subtitle: `Tipo: ${categoria.tipo}`,
    tipo: categoria.tipo
  }));
});

function handleSubmit() {
  // Validaciones básicas
  if (!product.value.nombre || !product.value.cod_producto || !product.value.precio_usd) {
    localErrors.value.general = 'Todos los campos obligatorios deben ser completados';
    return;
  }

  // Validar imagen si es nuevo producto
  if (!isEditing.value && !product.value.img) {
    localErrors.value.img = 'La imagen es requerida';
    return;
  }

  // Validaciones específicas por tipo de producto
  if (product.value.tipo_producto === 'noPreparado') {
    if (!noPreparadoData.value.cant_min || !noPreparadoData.value.costo_compra) {
      localErrors.value.general = 'Cantidad mínima y costo de compra son requeridos para productos no preparados';
      return;
    }
  }

  localErrors.value = {};
  emit('update:errors', {});

  // Construir objeto de datos según el tipo de producto
  let productData = {
    ...product.value,
    precio_usd: parseFloat(product.value.precio_usd)
  };

  if (product.value.tipo_producto === 'noPreparado') {
    productData = {
      ...productData,
      ...noPreparadoData.value,
      cant_min: parseInt(noPreparadoData.value.cant_min),
      cant_actual: parseInt(noPreparadoData.value.cant_actual || 0),
      costo_compra: parseFloat(noPreparadoData.value.costo_compra)
    };
  } else {
    productData = {
      ...productData,
      ...preparadoData.value
    };
  }

  emit('submit', productData);
  
  if (!isEditing.value) {
    resetForm();
  }
}

function resetForm() {
  product.value = {
    cod_producto: '',
    nombre: '',
    precio_usd: '',
    img: null,
    id_categoria: null,
    tipo_producto: 'noPreparado'
  };

  noPreparadoData.value = {
    cant_min: '',
    cant_actual: '',
    costo_compra: '',
    unidad_medida: 'unidad',
    Rif: ''
  };

  preparadoData.value = {
    descr_preparado: ''
  };

  imagePreview.value = null;
  searchQuery.value = '';
  localErrors.value = {};
  
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

function close() {
  emit('update:show', false);
  localErrors.value = {};
}

// Validaciones
function validatePrice(value) {
  if (!value) return 'Precio es requerido';
  const num = parseFloat(value);
  if (isNaN(num)) return 'Precio debe ser un número válido';
  if (num <= 0) return 'Precio debe ser mayor a 0';
  return true;
}

function validateCode(value) {
  if (!value) return 'Código es requerido';
  if (value.length < 3) return 'Código debe tener al menos 3 caracteres';
  if (value.length > 20) return 'Código debe tener máximo 20 caracteres';
  return true;
}

function validatePositiveNumber(value, fieldName) {
  if (!value) return `${fieldName} es requerido`;
  const num = parseFloat(value);
  if (isNaN(num)) return `${fieldName} debe ser un número válido`;
  if (num < 0) return `${fieldName} debe ser mayor o igual a 0`;
  return true;
}

function validateMinQuantity(value) {
  return validatePositiveNumber(value, 'Cantidad mínima');
}

function validateCost(value) {
  if (!value) return 'Costo de compra es requerido';
  const num = parseFloat(value);
  if (isNaN(num)) return 'Costo debe ser un número válido';
  if (num <= 0) return 'Costo debe ser mayor a 0';
  return true;
}
</script>

<template>
  <v-dialog 
    :model-value="show" 
    @update:model-value="$emit('update:show', $event)"  
    max-width="700"
    persistent
  >
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="me-2">
          {{ isEditing ? 'mdi-pencil' : 'mdi-plus' }}
        </v-icon>
        {{ title }}
        
        <!-- Indicador del tipo de producto -->
        <v-spacer></v-spacer>
        <v-chip
          v-if="product.tipo_producto"
          :color="product.tipo_producto === 'preparado' ? 'orange' : 'blue'"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ product.tipo_producto === 'preparado' ? 'mdi-chef-hat' : 'mdi-package-variant' }}
          </v-icon>
          {{ product.tipo_producto === 'preparado' ? 'Preparado' : 'No Preparado' }}
        </v-chip>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form @submit.prevent="handleSubmit">
          <!-- Error general -->
          <v-alert
            v-if="localErrors.general"
            type="error"
            variant="tonal"
            closable
            class="mb-4"
          >
            {{ localErrors.general }}
          </v-alert>

          <!-- Información básica del producto -->
          <div class="mb-6">
            <h3 class="text-h6 mb-4 d-flex align-center">
              <v-icon class="me-2">mdi-information</v-icon>
              Información Básica
            </h3>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="product.cod_producto"
                  label="Código del producto"
                  required
                  :rules="[validateCode]"
                  :error-messages="localErrors.cod_producto"
                  hint="Código único identificador del producto"
                  persistent-hint
                  :readonly="isEditing"
                  prepend-inner-icon="mdi-barcode"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="product.nombre"
                  label="Nombre del producto"
                  required
                  :rules="[v => !!v || 'Nombre es requerido']"
                  :error-messages="localErrors.nombre"
                  prepend-inner-icon="mdi-tag"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="product.precio_usd"
                  label="Precio USD"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  :rules="[validatePrice]"
                  :error-messages="localErrors.precio_usd"
                  prefix="$"
                  hint="Precio de venta del producto"
                  persistent-hint
                  prepend-inner-icon="mdi-currency-usd"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-autocomplete
                  v-model="product.id_categoria"
                  v-model:search="searchQuery"
                  :items="formattedCategorias"
                  item-title="text"
                  item-value="value"
                  label="Categoría"
                  clearable
                  :menu-props="{ maxHeight: '300px' }"
                  :error-messages="localErrors.id_categoria"
                  hint="Selecciona la categoría del producto"
                  persistent-hint
                  prepend-inner-icon="mdi-shape"
                  required
                  :rules="[v => !!v || 'Categoría es requerida']"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      :title="item.raw.title"
                      :subtitle="item.raw.subtitle"
                    >
                      <template v-slot:prepend>
                        <v-icon 
                          :color="item.raw.tipo === 'preparado' ? 'orange' : 'blue'"
                        >
                          {{ item.raw.tipo === 'preparado' ? 'mdi-chef-hat' : 'mdi-package-variant' }}
                        </v-icon>
                      </template>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </v-col>
            </v-row>
          </div>

          <!-- Campos específicos para productos NO PREPARADOS -->
          <div v-if="product.tipo_producto === 'noPreparado'" class="mb-6">
            <h3 class="text-h6 mb-4 d-flex align-center">
              <v-icon class="me-2" color="blue">mdi-package-variant</v-icon>
              Información de Inventario
            </h3>

            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="noPreparadoData.cant_min"
                  label="Cantidad mínima"
                  type="number"
                  min="0"
                  required
                  :rules="[validateMinQuantity]"
                  :error-messages="localErrors.cant_min"
                  hint="Stock mínimo requerido"
                  persistent-hint
                  prepend-inner-icon="mdi-alert"
                />
              </v-col>

              <v-col cols="12" md="4">
                <v-text-field
                  v-model="noPreparadoData.cant_actual"
                  label="Cantidad actual"
                  type="number"
                  min="0"
                  :rules="[v => validatePositiveNumber(v, 'Cantidad actual')]"
                  :error-messages="localErrors.cant_actual"
                  hint="Stock actual disponible"
                  persistent-hint
                  prepend-inner-icon="mdi-package"
                />
              </v-col>

              <v-col cols="12" md="4">
                <v-select
                  v-model="noPreparadoData.unidad_medida"
                  :items="unidadesMedida"
                  label="Unidad de medida"
                  required
                  :error-messages="localErrors.unidad_medida"
                  hint="Unidad de medida del producto"
                  persistent-hint
                  prepend-inner-icon="mdi-ruler"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="noPreparadoData.costo_compra"
                  label="Costo de compra"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  :rules="[validateCost]"
                  :error-messages="localErrors.costo_compra"
                  prefix="$"
                  hint="Costo unitario de compra"
                  persistent-hint
                  prepend-inner-icon="mdi-cash"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="noPreparadoData.Rif"
                  label="RIF del Proveedor"
                  :error-messages="localErrors.Rif"
                  hint="RIF del proveedor (opcional)"
                  persistent-hint
                  prepend-inner-icon="mdi-account-tie"
                  placeholder="J-12345678-9"
                />
              </v-col>
            </v-row>
          </div>

          <!-- Campos específicos para productos PREPARADOS -->
          <div v-if="product.tipo_producto === 'preparado'" class="mb-6">
            <h3 class="text-h6 mb-4 d-flex align-center">
              <v-icon class="me-2" color="orange">mdi-chef-hat</v-icon>
              Información del Producto Preparado
            </h3>

            <v-textarea
              v-model="preparadoData.descr_preparado"
              label="Descripción del producto"
              :error-messages="localErrors.descr_preparado"
              hint="Describe el producto preparado, ingredientes, etc."
              persistent-hint
              prepend-inner-icon="mdi-text"
              rows="3"
            />
          </div>

          <!-- Campo para imagen -->
          <div class="mb-4">
            <h3 class="text-h6 mb-4 d-flex align-center">
              <v-icon class="me-2">mdi-camera</v-icon>
              Imagen del Producto
            </h3>

            <v-row>
              <v-col cols="12" md="8">
                <v-file-input
                  ref="fileInput"
                  @change="handleFileUpload"
                  label="Seleccionar imagen"
                  accept="image/*"
                  prepend-icon="mdi-camera"
                  :error-messages="localErrors.img"
                  :required="!isEditing"
                  clearable
                  @click:clear="removeImage"
                  hint="Formatos soportados: JPG, PNG, GIF. Máximo 2MB"
                  persistent-hint
                />
              </v-col>
              
              <!-- Vista previa de la imagen -->
              <v-col cols="12" md="4" v-if="imagePreview">
                <v-card variant="tonal">
                  <v-card-subtitle>Vista previa</v-card-subtitle>
                  <v-img
                    :src="imagePreview"
                    height="120"
                    cover
                    class="ma-2 rounded"
                  />
                  <v-card-actions>
                    <v-btn
                      color="error"
                      size="small"
                      variant="outlined"
                      @click="removeImage"
                      block
                    >
                      <v-icon left>mdi-delete</v-icon>
                      Eliminar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </div>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-spacer></v-spacer>
        <v-btn 
          variant="outlined"
          @click="close"
        >
          Cancelar
        </v-btn>

        <v-btn 
          color="primary"
          @click="handleSubmit"
          :loading="loading"
        >
          <v-icon left>
            {{ isEditing ? 'mdi-content-save' : 'mdi-plus' }}
          </v-icon>
          {{ isEditing ? 'Actualizar' : 'Guardar' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-card-title {
  font-weight: 600;
}

.text-h6 {
  color: rgba(var(--v-theme-on-surface), 0.87);
}

:deep(.v-field__prepend-inner) {
  padding-top: 8px;
}
</style>