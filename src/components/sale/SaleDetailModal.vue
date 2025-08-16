<template>
  <v-dialog
    :model-value="show"
    @update:model-value="$emit('update:show', $event)"
    max-width="900px"
    persistent
    scrollable
  >
    <v-card>
      <!-- Header del modal -->
      <v-card-title class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-icon class="mr-3" color="primary">mdi-receipt</v-icon>
          <div>
            <div class="text-h5">Detalle de Venta</div>
            <div class="text-subtitle-1 text-grey" v-if="saleDetail">
              #{{ saleDetail.venta.id_venta }}
            </div>
          </div>
        </div>
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="closeModal"
          :disabled="loading"
        />
      </v-card-title>

      <v-divider />

      <!-- Contenido del modal -->
      <v-card-text class="pa-0">
        <!-- Loading state -->
        <div v-if="loading" class="text-center pa-8">
          <v-progress-circular
            indeterminate
            size="60"
            color="primary"
            class="mb-4"
          />
          <div class="text-h6">Cargando detalles de venta...</div>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="text-center pa-8">
          <v-icon size="60" color="error" class="mb-4">mdi-alert-circle</v-icon>
          <div class="text-h6 mb-2">Error al cargar detalles</div>
          <div class="text-body-1 text-grey mb-4">{{ error }}</div>
          <v-btn color="primary" @click="fetchSaleDetail">
            <v-icon left>mdi-refresh</v-icon>
            Reintentar
          </v-btn>
        </div>

        <!-- Content loaded -->
        <div v-else-if="saleDetail">
          <v-container fluid>
            <!-- Información general de la venta -->
            <v-row>
              <v-col cols="12">
                <v-card variant="tonal" color="primary" class="mb-4">
                  <v-card-title class="text-h6">
                    <v-icon left>mdi-information</v-icon>
                    Información General
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Fecha y Hora</div>
                          <div class="text-h6">
                            {{ saleDetail.fecha_formateada }} - {{ saleDetail.hora_formateada }}
                          </div>
                        </div>
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Tipo de Venta</div>
                          <v-chip
                            :color="saleDetail.venta.tipo === 'credito' ? 'orange' : 'green'"
                            variant="tonal"
                          >
                            <v-icon start>
                              {{ saleDetail.venta.tipo === 'credito' ? 'mdi-credit-card-clock' : 'mdi-cash' }}
                            </v-icon>
                            {{ saleDetail.venta.tipo === 'credito' ? 'Crédito' : 'De Contado' }}
                          </v-chip>
                        </div>
                      </v-col>
                      <v-col cols="12" md="6">
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Total USD</div>
                          <div class="text-h5 text-success">
                            {{ formatCurrency(saleDetail.venta.monto_total_usd) }}
                          </div>
                        </div>
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Total BS</div>
                          <div class="text-h6">
                            {{ formatCurrencyBS(saleDetail.venta.monto_total_bs) }}
                          </div>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Cliente y Tasa de cambio -->
            <v-row>
              <v-col cols="12" md="6">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-h6">
                    <v-icon left>mdi-account</v-icon>
                    Cliente
                  </v-card-title>
                  <v-card-text>
                    <div v-if="saleDetail.cliente">
                      <div class="mb-2">
                        <div class="text-subtitle-2 text-grey">Nombre</div>
                        <div class="text-h6">{{ saleDetail.cliente.nombre }}</div>
                      </div>
                      <div class="mb-2">
                        <div class="text-subtitle-2 text-grey">CI</div>
                        <div>{{ saleDetail.cliente.ci_cliente }}</div>
                      </div>
                      <div v-if="saleDetail.cliente.tlf" class="mb-2">
                        <div class="text-subtitle-2 text-grey">Teléfono</div>
                        <div>{{ saleDetail.cliente.tlf }}</div>
                      </div>
                      <div v-if="saleDetail.cliente.depto_escuela">
                        <div class="text-subtitle-2 text-grey">Departamento/Escuela</div>
                        <div>{{ saleDetail.cliente.depto_escuela }}</div>
                      </div>
                    </div>
                    <div v-else class="text-center py-4">
                      <v-icon size="48" color="grey-lighten-1">mdi-account-off</v-icon>
                      <div class="text-subtitle-1 text-grey mt-2">Cliente General</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>

              <v-col cols="12" md="6">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-h6">
                    <v-icon left>mdi-currency-usd</v-icon>
                    Tasa de Cambio
                  </v-card-title>
                  <v-card-text>
                    <div v-if="saleDetail.tasa_cambio">
                      <div class="mb-2">
                        <div class="text-subtitle-2 text-grey">Valor USD → BS</div>
                        <div class="text-h6">{{ formatCurrencyBS(saleDetail.tasa_cambio.valor_usd_bs) }}</div>
                      </div>
                      <div class="mb-2">
                        <div class="text-subtitle-2 text-grey">Origen</div>
                        <v-chip
                          :color="saleDetail.tasa_cambio.origen === 'BCV' ? 'blue' : 'orange'"
                          variant="tonal"
                          size="small"
                        >
                          {{ saleDetail.tasa_cambio.origen }}
                        </v-chip>
                      </div>
                    </div>
                    <div v-else class="text-center py-4">
                      <v-icon size="48" color="grey-lighten-1">mdi-currency-usd-off</v-icon>
                      <div class="text-subtitle-1 text-grey mt-2">Sin tasa registrada</div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Productos vendidos -->
            <v-row>
              <v-col cols="12">
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-h6">
                    <v-icon left>mdi-package-variant</v-icon>
                    Productos Vendidos
                  </v-card-title>
                  <v-card-text class="pa-0">
                    <v-data-table
                      :items="saleDetail.productos"
                      :headers="productHeaders"
                      density="comfortable"
                      :items-per-page="-1"
                      hide-default-footer
                    >
                      <!-- Columna de imagen -->
                      <template v-slot:item.producto.img="{ item }">
                        <v-avatar size="40" class="ma-1">
                          <v-img
                            v-if="item.producto.img"
                            :src="item.producto.img"
                            :alt="item.producto.nombre"
                            cover
                          />
                          <v-icon v-else color="grey-lighten-1" size="small">
                            mdi-image-off
                          </v-icon>
                        </v-avatar>
                      </template>

                      <!-- Columna de precio unitario -->
                      <template v-slot:item.detalle_venta.precio_unitario="{ item }">
                        <span class="font-weight-medium">
                          {{ formatCurrency(item.detalle_venta.precio_unitario) }}
                        </span>
                      </template>

                      <!-- Columna de cantidad -->
                      <template v-slot:item.detalle_venta.cantidad_producto="{ item }">
                        <v-chip color="primary" variant="tonal" size="small">
                          {{ item.detalle_venta.cantidad_producto }}
                        </v-chip>
                      </template>

                      <!-- Columna de subtotal -->
                      <template v-slot:item.subtotal="{ item }">
                        <span class="font-weight-medium text-success">
                          {{ formatCurrency(item.detalle_venta.precio_unitario * item.detalle_venta.cantidad_producto) }}
                        </span>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- Información de pago -->
            <v-row>
              <v-col cols="12">
                <v-card variant="tonal" color="success" class="mb-4">
                  <v-card-title class="text-h6">
                    <v-icon left>mdi-credit-card</v-icon>
                    Información de Pago
                  </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="4">
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Método de Pago</div>
                          <v-chip
                            :color="getPaymentMethodColor(saleDetail.pago.metodo_pago)"
                            variant="tonal"
                            class="mt-1"
                          >
                            <v-icon start>{{ getPaymentMethodIcon(saleDetail.pago.metodo_pago) }}</v-icon>
                            {{ formatPaymentMethod(saleDetail.pago.metodo_pago) }}
                          </v-chip>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Monto</div>
                          <div class="text-h6">{{ formatCurrencyBS(saleDetail.pago.monto) }}</div>
                        </div>
                      </v-col>
                      <v-col cols="12" md="4">
                        <div class="mb-3">
                          <div class="text-subtitle-2 text-grey">Fecha de Pago</div>
                          <div>{{ formatDate(saleDetail.pago.fecha_pago) }}</div>
                        </div>
                      </v-col>
                    </v-row>
                    
                    <!-- Referencia y teléfono si existen -->
                    <v-row v-if="saleDetail.pago.referencia || saleDetail.pago.num_tefl">
                      <v-col cols="12" md="6" v-if="saleDetail.pago.referencia">
                        <div class="text-subtitle-2 text-grey">Referencia</div>
                        <div class="font-weight-medium">{{ saleDetail.pago.referencia }}</div>
                      </v-col>
                      <v-col cols="12" md="6" v-if="saleDetail.pago.num_tefl">
                        <div class="text-subtitle-2 text-grey">Teléfono</div>
                        <div class="font-weight-medium">{{ saleDetail.pago.num_tefl }}</div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-card-text>

      <!-- Actions -->
      <v-card-actions class="pa-4">
        <v-spacer />
        <v-btn
          variant="text"
          @click="closeModal"
          :disabled="loading"
        >
          Cerrar
        </v-btn>
        <v-btn
          color="primary"
          variant="tonal"
          @click="printSale"
          :disabled="loading || !saleDetail"
        >
          <v-icon left>mdi-printer</v-icon>
          Imprimir
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import api from '@/api/api';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  saleId: {
    type: [Number, String],
    default: null
  }
});

const emit = defineEmits(['update:show']);

const { showSnackbar } = useSnackbar();

// Estado del componente
const saleDetail = ref(null);
const loading = ref(false);
const error = ref(null);

// Headers para la tabla de productos
const productHeaders = [
  { title: 'Imagen', key: 'producto.img', sortable: false, width: '80px' },
  { title: 'Código', key: 'producto.cod_producto', sortable: false },
  { title: 'Nombre', key: 'producto.nombre', sortable: false },
  { title: 'Precio Unitario', key: 'detalle_venta.precio_unitario', sortable: false },
  { title: 'Cantidad', key: 'detalle_venta.cantidad_producto', sortable: false },
  { title: 'Subtotal', key: 'subtotal', sortable: false }
];

// Watcher para cargar datos cuando se abre el modal
watch(() => props.show, (newVal) => {
  if (newVal && props.saleId) {
    fetchSaleDetail();
  } else if (!newVal) {
    // Limpiar datos cuando se cierra
    saleDetail.value = null;
    error.value = null;
  }
});

// Función para obtener detalles de la venta
async function fetchSaleDetail() {
  if (!props.saleId) return;
  
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.get(`/ventas/detalle/${props.saleId}`);
    saleDetail.value = response.data;
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al cargar los detalles de la venta';
    showSnackbar(error.value, 'error');
  } finally {
    loading.value = false;
  }
}

// Funciones de formato
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(amount);
}

function formatCurrencyBS(amount) {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'VES',
    minimumFractionDigits: 2
  }).format(amount);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('es-VE');
}

function formatPaymentMethod(method) {
  const methods = {
    'efectivo_bs': 'Efectivo BS',
    'efectivo_usd': 'Efectivo USD',
    'pago_movil': 'Pago Móvil',
    'debito': 'Débito',
    'transferencia': 'Transferencia'
  };
  return methods[method] || method;
}

function getPaymentMethodIcon(method) {
  const icons = {
    'efectivo_bs': 'mdi-cash',
    'efectivo_usd': 'mdi-currency-usd',
    'pago_movil': 'mdi-cellphone',
    'debito': 'mdi-credit-card',
    'transferencia': 'mdi-bank-transfer'
  };
  return icons[method] || 'mdi-credit-card';
}

function getPaymentMethodColor(method) {
  const colors = {
    'efectivo_bs': 'green',
    'efectivo_usd': 'blue',
    'pago_movil': 'purple',
    'debito': 'orange',
    'transferencia': 'teal'
  };
  return colors[method] || 'grey';
}

// Funciones de acciones
function closeModal() {
  emit('update:show', false);
}

function printSale() {
  // TODO: Implementar funcionalidad de impresión
  console.log('Imprimir venta:', saleDetail.value?.venta.id_venta);
  showSnackbar('Funcionalidad de impresión pendiente de implementar', 'info');
}
</script>

<style scoped>
.v-card-title {
  position: sticky;
  top: 0;
  z-index: 1;
  background: rgb(var(--v-theme-surface));
}

.v-dialog .v-card {
  height: 90vh;
}
</style>