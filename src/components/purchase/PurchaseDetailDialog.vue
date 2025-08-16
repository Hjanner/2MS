<script setup>
import { computed } from 'vue';
import { formatCurrencyBs } from '@/utils/formatters';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  purchaseDetails: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:show']);

const isOpen = computed({
  get() {
    return props.show;
  },
  set(value) {
    emit('update:show', value);
  }
});

// Computed para obtener los productos formateados para la tabla
const productosFormateados = computed(() => {
  if (!props.purchaseDetails?.productos) return [];
  
  return props.purchaseDetails.productos.map(item => ({
    cod_producto: item.producto.cod_producto,
    nombre: item.producto.nombre,
    cantidad: item.movimiento.cant_movida,
    costo_unitario: item.movimiento.costo_unitario,
    subtotal: item.movimiento.cant_movida * item.movimiento.costo_unitario,
    unidad_medida: item.producto_no_preparado.unidad_medida
  }));
});

function closeDialog() {
  isOpen.value = false;
}
</script>

<template>
  <v-dialog
    v-model="isOpen"
    max-width="900"
    scrollable
    persistent
  >
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="mr-2">mdi-receipt</v-icon>
        Detalles de Compra #{{ purchaseDetails?.compra?.id_compra }}
        <v-spacer />
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="closeDialog"
        />
      </v-card-title>
      <v-divider />

      <v-card-text class="pa-6">
        <!-- Loading state -->
        <v-progress-linear
          v-if="loading"
          indeterminate
          color="primary"
          class="mb-4"
        />

        <div v-if="purchaseDetails">
          <!-- Información general -->
          <div class="mb-6">
            <h3 class="text-h6 mb-4">
              <v-icon class="mr-2">mdi-information</v-icon>
              Información General
            </h3>
            <v-row>
              <v-col cols="12" md="4">
                <v-card variant="tonal" class="pa-3">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Fecha</div>
                  <div class="text-body-1 font-weight-medium">
                    {{ purchaseDetails.fecha_formateada }}
                  </div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="tonal" class="pa-3">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">ID Compra</div>
                  <div class="text-body-1 font-weight-medium">
                    {{ purchaseDetails.compra.id_compra }}
                  </div>
                </v-card>
              </v-col>
              <v-col cols="12" md="4">
                <v-card variant="tonal" class="pa-3">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Gasto Total</div>
                  <div class="text-h6 text-success font-weight-bold">
                    {{ formatCurrencyBs(purchaseDetails.compra.gasto_total) }}
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </div>

          <!-- Información del proveedor -->
          <div class="mb-6">
            <h3 class="text-h6 mb-4">
              <v-icon class="mr-2">mdi-truck</v-icon>
              Información del Proveedor
            </h3>
            <v-card variant="outlined" class="pa-4">
              <v-row>
                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">RIF</div>
                  <div class="text-body-1 font-weight-medium">
                    {{ purchaseDetails.proveedor.Rif }}
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Razón Social</div>
                  <div class="text-body-1 font-weight-medium">
                    {{ purchaseDetails.proveedor.razon_social }}
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Teléfono</div>
                  <div class="text-body-1">
                    {{ purchaseDetails.proveedor.tfl || 'No disponible' }}
                  </div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Persona de Contacto</div>
                  <div class="text-body-1">
                    {{ purchaseDetails.proveedor.persona_contacto || 'No disponible' }}
                  </div>
                </v-col>
                <v-col cols="12">
                  <div class="text-subtitle-2 text-grey-darken-1 mb-1">Dirección</div>
                  <div class="text-body-1">
                    {{ purchaseDetails.proveedor.direccion || 'No disponible' }}
                  </div>
                </v-col>
              </v-row>
            </v-card>
          </div>

          <!-- Productos comprados -->
          <div v-if="productosFormateados.length">
            <h3 class="text-h6 mb-4">
              <v-icon class="mr-2">mdi-package-variant</v-icon>
              Productos Comprados ({{ productosFormateados.length }} items)
            </h3>
            <v-data-table
              :headers="[
                { title: 'Código', value: 'cod_producto', width: '120px' },
                { title: 'Producto', value: 'nombre' },
                { title: 'Cantidad', value: 'cantidad', align: 'center', width: '100px' },
                { title: 'Unidad', value: 'unidad_medida', align: 'center', width: '100px' },
                { title: 'Costo Unit.', value: 'costo_unitario', align: 'end', width: '120px' },
                { title: 'Subtotal', value: 'subtotal', align: 'end', width: '120px' }
              ]"
              :items="productosFormateados"
              hide-default-footer
              class="elevation-2"
            >
              <template #item.cod_producto="{ item }">
                <v-chip
                  size="small"
                  color="primary"
                  variant="outlined"
                >
                  {{ item.cod_producto }}
                </v-chip>
              </template>
              
              <template #item.cantidad="{ item }">
                <span class="font-weight-medium">{{ item.cantidad }}</span>
              </template>
              
              <template #item.unidad_medida="{ item }">
                <v-chip size="small" variant="tonal">
                  {{ item.unidad_medida }}
                </v-chip>
              </template>
              
              <template #item.costo_unitario="{ item }">
                {{ formatCurrencyBs(item.costo_unitario) }}
              </template>
              
              <template #item.subtotal="{ item }">
                <span class="font-weight-bold text-success">
                  {{ formatCurrencyBs(item.subtotal) }}
                </span>
              </template>
            </v-data-table>
            
            <!-- Total -->
            <v-card variant="tonal" color="success" class="mt-4">
              <v-card-text class="d-flex justify-space-between align-center">
                <span class="text-h6">Total de la Compra:</span>
                <span class="text-h5 font-weight-bold">
                  {{ formatCurrencyBs(purchaseDetails.compra.gasto_total) }}
                </span>
              </v-card-text>
            </v-card>
          </div>
        </div>

        <!-- Estado vacío -->
        <div v-else-if="!loading" class="text-center py-8">
          <v-icon size="64" color="grey-lighten-1">mdi-file-document-outline</v-icon>
          <p class="text-h6 text-grey-darken-1 mt-4">No se encontraron detalles</p>
        </div>
      </v-card-text>

      <v-divider />

      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          variant="elevated"
          @click="closeDialog"
        >
          Cerrar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-data-table {
  border-radius: 8px;
}
</style>