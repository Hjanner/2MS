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
  precio: '',
  id_categoria: null
});

const localErrors = ref({});        // Estado para los errores de la API
const searchQuery = ref('');       // Variable para la búsqueda de categorías
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
  if (!product.value.nombre || !product.value.cod_producto || !product.value.precio) return;

  localErrors.value = {};         //limpiar errores antes de enviar
  emit('update:errors', {});

  // Convertir precio a número
  const productData = {
    ...product.value,
    precio: parseFloat(product.value.precio)
  };

  emit('submit', productData);
  resetForm();  
}

function resetForm() {
  product.value = {
    cod_producto: '',
    nombre: '',
    precio: '',
    id_categoria: null
  };
  searchQuery.value = '';
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
            v-model="product.precio"
            label="Precio"
            type="number"
            step="0.01"
            min="0"
            required
            :rules="[validatePrice]"
            :error-messages="localErrors.precio"
            class="mb-4"
            prefix="Bs."
            hint="Precio de venta del producto"
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