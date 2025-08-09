<script setup>
import { ref, watch, computed, nextTick } from 'vue';
import { formatCurrencyBs } from '@/utils/formatters';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Compra'
  },
  proveedores: {
    type: Array,
    default: () => []
  },
  productos: {
    type: Array,
    default: () => []
  },
  errors: {
    type: Object,
    default: () => ({})
  },
  mode: {
    type: String,
    default: 'add', // 'add' | 'edit'
    validator: (value) => ['add', 'edit'].includes(value)
  },
  compraData: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['submit', 'update:show']);

// Formulario reactivo
const form = ref({
  fecha: new Date().toISOString().split('T')[0], // Fecha actual por defecto
  Rif: '',
  gasto_total: 0,
  productos: []
});

// Referencia al formulario para validación
const formRef = ref(null);

// Producto temporal para agregar a la lista
const nuevoProducto = ref({
  cod_producto: '',
  cantidad: 1,
  costo_unitario: 0
});

// Reglas de validación
const rules = {
  fecha: [
    v => !!v || 'La fecha es requerida',
    v => !isNaN(Date.parse(v)) || 'Fecha inválida'
  ],
  Rif: [
    v => !!v || 'El proveedor es requerido'
  ],
  gasto_total: [
    v => v >= 0 || 'El gasto total debe ser mayor o igual a 0'
  ]
};

// Computed para calcular el total automáticamente
const gastoTotalCalculado = computed(() => {
  return form.value.productos.reduce((total, producto) => {
    return total + (producto.cantidad * producto.costo_unitario);
  }, 0);
});

// Watch para actualizar el gasto total automáticamente
watch(gastoTotalCalculado, (newTotal) => {
  form.value.gasto_total = newTotal;
});

// Watch para cargar datos cuando se abre el modal en modo edición
watch(() => props.show, (newValue) => {
  if (newValue) {
    if (props.mode === 'edit' && props.compraData) {
      loadCompraData();
    } else {
      resetForm();
    }
  }
});

// Cargar datos de la compra para edición
function loadCompraData() {
  if (props.compraData) {
    form.value = {
      fecha: props.compraData.fecha,
      Rif: props.compraData.Rif,
      gasto_total: props.compraData.gasto_total,
      productos: props.compraData.productos ? [...props.compraData.productos] : []
    };
  }
}

// Resetear formulario
function resetForm() {
  form.value = {
    fecha: new Date().toISOString().split('T')[0],
    Rif: '',
    gasto_total: 0,
    productos: []
  };
  nuevoProducto.value = {
    cod_producto: '',
    cantidad: 1,
    costo_unitario: 0
  };
  
  nextTick(() => {
    if (formRef.value) {
      formRef.value.resetValidation();
    }
  });
}

// Agregar producto a la lista
function agregarProducto() {
  if (!nuevoProducto.value.cod_producto) {
    return;
  }

  // Verificar si el producto ya está en la lista
  const productoExistente = form.value.productos.find(
    p => p.cod_producto === nuevoProducto.value.cod_producto
  );

  if (productoExistente) {
    // Si existe, actualizar cantidad
    productoExistente.cantidad += nuevoProducto.value.cantidad;
    productoExistente.costo_unitario = nuevoProducto.value.costo_unitario;
  } else {
    // Si no existe, agregar nuevo
    const producto = props.productos.find(p => p.cod_producto === nuevoProducto.value.cod_producto);
    form.value.productos.push({
      cod_producto: nuevoProducto.value.cod_producto,
      nombre: producto?.nombre || '',
      cantidad: nuevoProducto.value.cantidad,
      costo_unitario: nuevoProducto.value.costo_unitario
    });
  }

  // Resetear formulario de producto
  nuevoProducto.value = {
    cod_producto: '',
    cantidad: 1,
    costo_unitario: 0
  };
}

// Eliminar producto de la lista
function eliminarProducto(index) {
  form.value.productos.splice(index, 1);
}

// Validar y enviar formulario
async function submitForm() {
  if (!formRef.value) return;
  
  const { valid } = await formRef.value.validate();
  
  if (valid && form.value.productos.length > 0) {
    emit('submit', { ...form.value });
  } else if (form.value.productos.length === 0) {
    // Mostrar error si no hay productos
    alert('Debe agregar al menos un producto a la compra');
  }
}

// Cerrar modal
function closeDialog() {
  emit('update:show', false);
}

// Obtener nombre del proveedor
function getProveedorNombre(rif) {
  const proveedor = props.proveedores.find(p => p.Rif === rif);
  return proveedor?.razon_social || '';
}

// Obtener nombre del producto
function getProductoNombre(cod_producto) {
  const producto = props.productos.find(p => p.cod_producto === cod_producto);
  return producto?.nombre || '';
}
</script>

<template>
  <v-dialog
    :model-value="show"
    @update:model-value="closeDialog"
    max-width="900"
    persistent
    scrollable
  >
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">
          {{ mode === 'add' ? 'mdi-plus' : 'mdi-pencil' }}
        </v-icon>
        {{ title }}
        <v-spacer />
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="closeDialog"
          :disabled="loading"
        />
      </v-card-title>

      <v-divider />

      <v-card-text class="pa-6">
        <v-form ref="formRef" @submit.prevent="submitForm">
          <!-- Información básica de la compra -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title class="text-subtitle-1 py-3">
              <v-icon class="mr-2" size="small">mdi-information</v-icon>
              Información de la Compra
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.fecha"
                    label="Fecha de Compra"
                    type="date"
                    :rules="rules.fecha"
                    :error-messages="errors.fecha"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-calendar"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="form.Rif"
                    :items="proveedores"
                    item-value="Rif"
                    item-title="razon_social"
                    label="Proveedor"
                    :rules="rules.Rif"
                    :error-messages="errors.Rif"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-truck-delivery"
                  >
                    <template #item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template #prepend>
                          <v-icon>mdi-truck-delivery</v-icon>
                        </template>
                        <v-list-item-title>{{ item.raw.razon_social }}</v-list-item-title>
                        <v-list-item-subtitle>RIF: {{ item.raw.Rif }}</v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-col>

                <v-col cols="12">
                  <v-text-field
                    v-model.number="form.gasto_total"
                    label="Gasto Total (BS)"
                    type="number"
                    step="0.01"
                    :rules="rules.gasto_total"
                    :error-messages="errors.gasto_total"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-currency-usd"
                    readonly
                    hint="Se calcula automáticamente según los productos agregados"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Agregar productos -->
          <v-card variant="outlined" class="mb-6">
            <v-card-title class="text-subtitle-1 py-3">
              <v-icon class="mr-2" size="small">mdi-package-variant</v-icon>
              Agregar Productos
            </v-card-title>
            <v-card-text>
              <v-row align="center">
                <v-col cols="12" md="4">
                  <v-select
                    v-model="nuevoProducto.cod_producto"
                    :items="productos"
                    item-value="cod_producto"
                    item-title="nombre"
                    label="Producto"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-package"
                  >
                    <template #item="{ props, item }">
                      <v-list-item v-bind="props">
                        <template #prepend>
                          <v-icon>mdi-package</v-icon>
                        </template>
                        <v-list-item-title>{{ item.raw.nombre }}</v-list-item-title>
                        <v-list-item-subtitle>Código: {{ item.raw.cod_producto }}</v-list-item-subtitle>
                      </v-list-item>
                    </template>
                  </v-select>
                </v-col>

                <v-col cols="12" md="3">
                  <v-text-field
                    v-model.number="nuevoProducto.cantidad"
                    label="Cantidad"
                    type="number"
                    min="1"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-counter"
                  />
                </v-col>

                <v-col cols="12" md="3">
                  <v-text-field
                    v-model.number="nuevoProducto.costo_unitario"
                    label="Costo Unitario (BS)"
                    type="number"
                    step="0.01"
                    min="0"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-currency-usd"
                  />
                </v-col>

                <v-col cols="12" md="2">
                  <v-btn
                    @click="agregarProducto"
                    color="primary"
                    block
                    variant="elevated"
                    prepend-icon="mdi-plus"
                  >
                    Agregar
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Lista de productos agregados -->
          <v-card variant="outlined" v-if="form.productos.length > 0">
            <v-card-title class="text-subtitle-1 py-3">
              <v-icon class="mr-2" size="small">mdi-format-list-bulleted</v-icon>
              Productos en la Compra ({{ form.productos.length }})
            </v-card-title>
            <v-card-text class="pa-0">
              <v-data-table
                :headers="[
                  { title: 'Producto', value: 'nombre', sortable: false },
                  { title: 'Código', value: 'cod_producto', sortable: false },
                  { title: 'Cantidad', value: 'cantidad', sortable: false },
                  { title: 'Costo Unitario', value: 'costo_unitario', sortable: false },
                  { title: 'Subtotal', value: 'subtotal', sortable: false },
                  { title: 'Acciones', value: 'actions', sortable: false, align: 'center' }
                ]"
                :items="form.productos.map((p, index) => ({
                  ...p,
                  subtotal: p.cantidad * p.costo_unitario,
                  index
                }))"
                hide-default-footer
                class="elevation-0"
              >
                <template #item.costo_unitario="{ item }">
                    {{ formatCurrencyBs(item.costo_unitario.toFixed(2)) }}
                </template>

                <template #item.subtotal="{ item }">
                  <span class="font-weight-medium text-success">
                    {{ formatCurrencyBs(item.subtotal.toFixed(2)) }}                    
                  </span>
                </template>

                <template #item.actions="{ item }">
                  <v-btn
                    icon="mdi-delete"
                    size="small"
                    variant="text"
                    color="error"
                    @click="eliminarProducto(item.index)"
                  />
                </template>
              </v-data-table>

              <v-divider />

              <!-- Total -->
              <div class="pa-4 text-right">
                <div class="text-h6 d-flex align-center justify-end">
                  <!-- <v-icon class="mr-2" color="success">mdi-currency-usd</v-icon> -->
                  <span class="text-success">
                    Total: {{ formatCurrencyBs(gastoTotalCalculado.toFixed(2)) }}
                  </span>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Mensaje si no hay productos -->
          <v-card variant="outlined" v-else>
            <v-card-text class="text-center pa-8">
              <v-icon size="64" color="grey-lighten-2">
                mdi-package-variant-closed
              </v-icon>
              <div class="text-h6 text-grey-lighten-1 mt-2">
                No hay productos agregados
              </div>
              <div class="text-body-2 text-grey-lighten-1">
                Agrega productos a la compra usando el formulario de arriba
              </div>
            </v-card-text>
          </v-card>

          <!-- Errores generales -->
          <v-alert
            v-if="errors.general"
            type="error"
            variant="tonal"
            class="mt-4"
          >
            {{ errors.general }}
          </v-alert>
        </v-form>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn
          variant="text"
          @click="closeDialog"
          :disabled="loading"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="primary"
          @click="submitForm"
          :loading="loading"
          :disabled="form.productos.length === 0"
        >
          {{ mode === 'add' ? 'Registrar Compra' : 'Actualizar Compra' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
:deep(.v-data-table) {
  border-radius: 0;
}

:deep(.v-data-table .v-data-table__wrapper) {
  border-radius: 0;
}
</style>