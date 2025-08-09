<script setup>
import { computed } from 'vue';
import { validateRequired, validateCode, validatePrice } from '@/utils/validators.js';

const props = defineProps({
  modelValue: Object,
  categorias: Array,
  errors: Object,
  isEditing: Boolean
});

const emit = defineEmits(['update:modelValue']);

const product = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const validationRules = {
  cod_producto: [validateCode],
  nombre: [validateRequired('Nombre')],
  precio_usd: [validatePrice],
  id_categoria: [validateRequired('Categoría')]
};

const formattedCategorias = computed(() => {
  return props.categorias.map(categoria => ({
    value: categoria.id_categoria,
    text: `${categoria.descr} (${categoria.tipo})`,
    title: categoria.descr,
    subtitle: `Tipo: ${categoria.tipo}`,
    tipo: categoria.tipo
  }));
});
</script>

<template>
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
          :rules="validationRules.cod_producto"
          :error-messages="errors.cod_producto"
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
          :rules="validationRules.nombre"
          :error-messages="errors.nombre"
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
          :rules="validationRules.precio_usd"
          :error-messages="errors.precio_usd"
          prefix="$"
          hint="Precio de venta del producto"
          persistent-hint
          prepend-inner-icon="mdi-currency-usd"
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-autocomplete
          v-model="product.id_categoria"
          :items="formattedCategorias"
          item-title="text"
          item-value="value"
          label="Categoría"
          clearable
          :menu-props="{ maxHeight: '300px' }"
          :error-messages="errors.id_categoria"
          hint="Selecciona la categoría del producto"
          persistent-hint
          prepend-inner-icon="mdi-shape"
          required
          :rules="validationRules.id_categoria"
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
</template>