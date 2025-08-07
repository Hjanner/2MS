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
  }
});

const emit = defineEmits(['submit', 'update:show', 'update:errors']);

const product = ref({
  cod_producto: '',
  nombre: '',
  precio_usd: '',
  img: null,
  id_categoria: null
});

const localErrors = ref({});        // Estado para los errores de la API
const searchQuery = ref('');        // Variable para la búsqueda de categorías
const imagePreview = ref(null);     // Para mostrar vista previa de la imagen
const fileInput = ref(null);        // Referencia al input de archivo
const isEditing = computed(() => !!props.productData);    //// Propiedad computada para determinar el modo del formulario

//manejo de errores desde la api
watch(() => props.errors, (newErrors) => {
    localErrors.value = { ...newErrors };
}, { immediate: true });

// Actualizar el formulario cuando cambia productData
watch(() => props.productData, (newVal) => {
  if (newVal) {
    product.value = { ...newVal };
  } else {
    resetForm();
  }
}, { immediate: true });


function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();

  reader.onload = (e) => {
    product.value.img = e.target.result; // Esto será un string base64
    imagePreview.value = e.target.result;
  };
  
  reader.readAsDataURL(file);

  // Validar tipo de archivo
  // if (!file.type.match('image.*')) {
  //   localErrors.value.img = 'Solo se permiten imágenes';
  //   return;
  // }

  // // Validar tamaño (ejemplo: máximo 2MB)
  // if (file.size > 2 * 1024 * 1024) {
  //   localErrors.value.img = 'La imagen no debe exceder 2MB';
  //   return;
  // }

  // // Crear vista previa
  // const reader = new FileReader();
  // reader.onload = (e) => {
  //   imagePreview.value = e.target.result;
  // };
  // reader.readAsDataURL(file);

  // // Asignar el archivo al objeto producto
  // product.value.img = file;
  // localErrors.value.img = null;
}

function removeImage() {
  imagePreview.value = null;
  product.value.img = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

// Filtrar categorías basado en la búsqueda
const filteredCategorias = computed(() => {
  if (!searchQuery.value) return categorias.value;
  
  const query = searchQuery.value.toLowerCase();
  return categorias.value.filter(categoria => 
    categoria.text.toLowerCase().includes(query)
  );
});

// Formatear categorías para el autocomplete
const formattedCategorias = computed(() => {
  return props.categorias.map(categoria => ({
    value: categoria.id_categoria,
    text: `${categoria.descr} (${categoria.tipo})`,
    title: categoria.descr,
    subtitle: `Tipo: ${categoria.tipo}`
  }));
});

function handleSubmit() {
  if (!product.value.nombre || !product.value.cod_producto || !product.value.precio_usd) return;

  localErrors.value = {};         //limpiar errores antes de enviar
  emit('update:errors', {});

  if (!isEditing.value && !product.value.img) {           // Validar imagen si es nuevo producto
    localErrors.value.img = 'La imagen es requerida';
    return;
  }

  const productData = new FormData(); // Usar FormData para enviar archivos
  productData.append('cod_producto', product.value.cod_producto);
  productData.append('nombre', product.value.nombre);
  productData.append('precio_usd', parseFloat(product.value.precio_usd));
  if (product.value.id_categoria) {
    productData.append('id_categoria', product.value.id_categoria);
  }
  if (product.value.img) {            // Agregar imagen si existe
    productData.append('img', product.value.img);
  }

  // emit('submit', productData);
  emit('submit', {
    ...product.value,
    precio_usd: parseFloat(product.value.precio_usd)
  });
  resetForm();  
}

function resetForm() {
  product.value = {
    cod_producto: '',
    nombre: '',
    precio_usd: '',
    id_categoria: null
  };
  imagePreview.value = null;
  searchQuery.value = '';
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

function close() {
  emit('update:show', false);
  localErrors.value = {};
}

// Validaciones personalizadas
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
</script>

<template>
  <v-dialog 
    :model-value="show" 
    @update:model-value="$emit('update:show', $event)"  
    max-width="600"
  >
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="product.cod_producto"
            label="Código del producto"
            required
            :rules="[validateCode]"
            :error-messages="localErrors.cod_producto"
            class="mb-4"
            hint="Código único identificador del producto"
            persistent-hint
            :readonly="isEditing"
          />

          <v-text-field
            v-model="product.nombre"
            label="Nombre del producto"
            required
            :rules="[v => !!v || 'Nombre es requerido']"
            :error-messages="localErrors.nombre"
            class="mb-4"
          />

          <v-text-field
            v-model="product.precio_usd"
            label="Precio USD"
            type="number"
            step="0.01"
            min="0"
            required
            :rules="[validatePrice]"
            :error-messages="localErrors.precio_usd"
            class="mb-4"
            prefix="Bs."
            hint="Precio de venta del producto (USD)"
            persistent-hint
          />
          
          <!-- Select con buscador para categorías -->
          <v-autocomplete
            v-model="product.id_categoria"
            v-model:search="searchQuery"
            :items="formattedCategorias"
            item-title="text"
            item-value="value"
            label="Seleccionar categoría"
            clearable
            :menu-props="{ maxHeight: '300px' }"
            :error-messages="localErrors.id_categoria"
            hint="Opcional: Categoría del producto"
            persistent-hint
            class="mb-8"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item
                v-bind="props"
                :title="item.raw.title"
                :subtitle="item.raw.subtitle"
              >
                <template v-slot:prepend>
                  <v-icon 
                    :color="item.raw.subtitle.includes('preparado') ? 'orange' : 'blue'"
                  >
                    {{ item.raw.subtitle.includes('preparado') ? 'mdi-chef-hat' : 'mdi-package-variant' }}
                  </v-icon>
                </template>
              </v-list-item>
            </template>

            <template v-slot:no-data>
              <v-list-item>
                <v-list-item-title>
                  {{ loadingCategorias ? 'Cargando categorías...' : 'No se encontraron categorías' }}
                </v-list-item-title>
              </v-list-item>
            </template>
          </v-autocomplete>

          <!-- Campo para subir imagen -->
          <v-row class="mb-4">
            <v-col cols="12">
              <v-file-input
                ref="fileInput"
                v-model="product.img"
                @change="handleFileUpload"
                label="Imagen del producto"
                accept="image/*"
                prepend-icon="mdi-camera"
                :error-messages="localErrors.img"
                :required="!isEditing"
                :clearable="!isEditing"
                @click:clear="removeImage"
              ></v-file-input>
            </v-col>
            
            <!-- Vista previa de la imagen -->
            <v-col cols="12" v-if="imagePreview || (isEditing && productData.img)">
              <v-card class="pa-2" elevation="2">
                <v-card-title class="text-subtitle-1">Vista previa</v-card-title>
                <v-img
                  :src="imagePreview || productData.img"
                  max-height="200"
                  contain
                  class="mb-2"
                ></v-img>
                <v-btn
                  v-if="!isEditing"
                  color="error"
                  size="small"
                  @click="removeImage"
                >
                  <v-icon left>mdi-delete</v-icon>
                  Eliminar imagen
                </v-btn>
              </v-card>
            </v-col>
          </v-row>
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