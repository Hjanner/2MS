<script setup>
import { ref, computed } from 'vue';
import ReloadButton from '@/components/common/ReloadButton.vue';

const props = defineProps({
  ventas: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['refresh', 'view-details']);

// Headers para la tabla
const headers = [
  { title: 'ID Venta', key: 'id_venta', sortable: true },
  { title: 'Fecha/Hora', key: 'fecha_formateada', sortable: true },
  { title: 'Tipo', key: 'tipo', sortable: true },
  { title: 'Monto USD', key: 'monto_total_usd', sortable: true },
  { title: 'Monto BS', key: 'monto_total_bs', sortable: true },
  { title: 'Productos', key: 'cantidad_productos', sortable: true },
  { title: 'Cliente', key: 'cliente', sortable: false },
//   { title: 'Método Pago', key: 'metodo_pago', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false, width: '100px' }
];

// Computadas para métricas
const totalVentasUSD = computed(() => {
  return props.ventas.reduce((total, venta) => total + venta.monto_total_usd, 0);
});

const totalVentasBS = computed(() => {
  return props.ventas.reduce((total, venta) => total + venta.monto_total_bs, 0);
});

const totalProductosVendidos = computed(() => {
  return props.ventas.reduce((total, venta) => total + venta.cantidad_productos, 0);
});

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

function viewDetails(venta) {
  emit('view-details', venta);
}
</script>

<template>
  <div class="sales-list">
    <!-- Métricas de ventas -->
    <v-row class="mb-4">
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="primary" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-cart</v-icon>
            <div class="text-h6">Total Ventas</div>
            <div class="text-h4">{{ ventas.length }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="success" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-currency-usd</v-icon>
            <div class="text-h6">Total USD</div>
            <div class="text-h4">{{ formatCurrency(totalVentasUSD) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="warning" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-cash</v-icon>
            <div class="text-h6">Total BS</div>
            <div class="text-h4">{{ formatCurrencyBS(totalVentasBS) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="info" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-package-variant</v-icon>
            <div class="text-h6">Productos Vendidos</div>
            <div class="text-h4">{{ totalProductosVendidos }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabla de ventas -->
    <v-data-table
      :headers="headers"
      :items="ventas"
      :loading="loading"
      loading-text="Cargando ventas..."
      no-data-text="No hay ventas registradas"
      :items-per-page="10"
      :items-per-page-options="[5, 10, 25, 50, -1]"
      class="elevation-1"
    >
      <!-- Columna de ID de venta -->
      <template v-slot:item.id_venta="{ item }">
        <span class="font-weight-medium text-primary">
          #{{ item.id_venta }}
        </span>
      </template>

      <!-- Columna de fecha -->
      <template v-slot:item.fecha_formateada="{ item }">
        <div>
          <div class="font-weight-medium">{{ item.fecha_formateada }}</div>
          <div class="text-caption text-grey">{{ item.hora_formateada }}</div>
        </div>
      </template>

      <!-- Columna de tipo de venta -->
      <template v-slot:item.tipo="{ item }">
        <v-chip
          :color="item.tipo === 'credito' ? 'orange' : 'green'"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ item.tipo === 'credito' ? 'mdi-credit-card-clock' : 'mdi-cash' }}
          </v-icon>
          {{ item.tipo === 'credito' ? 'Crédito' : 'De Contado' }}
        </v-chip>
      </template>

      <!-- Columna de monto USD -->
      <template v-slot:item.monto_total_usd="{ item }">
        <span class="font-weight-medium text-success">
          {{ formatCurrency(item.monto_total_usd) }}
        </span>
      </template>

      <!-- Columna de monto BS -->
      <template v-slot:item.monto_total_bs="{ item }">
        <span class="font-weight-medium">
          {{ formatCurrencyBS(item.monto_total_bs) }}
        </span>
      </template>

      <!-- Columna de cantidad de productos -->
      <template v-slot:item.cantidad_productos="{ item }">
        <v-chip
          color="primary"
          variant="tonal"
          size="small"
        >
          <v-icon start>mdi-package-variant</v-icon>
          {{ item.cantidad_productos }}
        </v-chip>
      </template>

      <!-- Columna de cliente -->
      <template v-slot:item.cliente="{ item }">
        <div v-if="item.cliente">
          <div class="font-weight-medium">{{ item.cliente.nombre }}</div>
          <div class="text-caption text-grey">{{ item.cliente.ci_cliente }}</div>
        </div>
        <v-chip v-else color="grey" variant="tonal" size="small">
          <v-icon start>mdi-account-off</v-icon>
          Cliente General
        </v-chip>
      </template>

      <!-- Columna de método de pago -->
      <!-- <template v-slot:item.metodo_pago="{ item }">
        <v-chip
          :color="getPaymentMethodColor(item.pago?.metodo_pago || 'Efectivo BS' )"
          variant="tonal"
          size="small"
        >
          <v-icon start>{{ getPaymentMethodIcon(item.pago?.metodo_pago || 0) }}</v-icon>
          {{ formatPaymentMethod(item.pago.metodo_pago) }}
        </v-chip>
      </template> -->

      <!-- Columna de acciones -->
      <template v-slot:item.actions="{ item }">
        <v-tooltip text="Ver detalles de venta">
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              icon="mdi-eye-outline"
              size="small"
              color="primary"
              variant="tonal"
              @click="viewDetails(item)"
            />
          </template>
        </v-tooltip>
      </template>

      <!-- Template cuando no hay datos -->
      <template v-slot:no-data>
        <div class="text-center pa-4">
          <v-icon size="48" color="grey-lighten-1" class="mb-4">
            mdi-cart-off
          </v-icon>
          <div class="text-h6 mb-2">No hay ventas registradas</div>
          <div class="text-subtitle-1 text-grey">
            Las ventas aparecerán aquí cuando se registren en el sistema.
          </div>
        </div>
      </template>
    </v-data-table>

    <!-- Botón de actualizar lista -->
    <ReloadButton :loading="loading" @click="$emit('refresh')" />
  </div>
</template>



<style scoped>
.sales-list {
  width: 100%;
}

.btn-action {
  gap: 4px;
}
</style>