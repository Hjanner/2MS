<template>
  <div class="debt-list">
    <!-- Métricas de deudas -->
    <v-row class="mb-4">
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="warning" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-account-credit-card</v-icon>
            <div class="text-h6">Total Créditos</div>
            <div class="text-h4">{{ creditos.length }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="error" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-currency-usd-off</v-icon>
            <div class="text-h6">Total Adeudado</div>
            <div class="text-h4">{{ formatCurrency(totalAdeudado) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="success" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-cash-check</v-icon>
            <div class="text-h6">Total Pagado</div>
            <div class="text-h4">{{ formatCurrency(totalPagado) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card class="text-center pa-4" color="info" variant="tonal">
          <v-card-text>
            <v-icon size="40" class="mb-2">mdi-account-multiple</v-icon>
            <div class="text-h6">Clientes con Deuda</div>
            <div class="text-h4">{{ clientesConDeuda }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabla de deudas -->
    <v-data-table
      :headers="headers"
      :items="creditos"
      :loading="loading"
      loading-text="Cargando créditos..."
      no-data-text="No hay créditos registrados"
      :items-per-page="10"
      :items-per-page-options="[5, 10, 25, 50, -1]"
      class="elevation-1"
    >
      <!-- Columna de ID de crédito -->
      <template v-slot:item.id_credito="{ item }">
        <span class="font-weight-medium text-primary">
          #{{ item.id_credito }}
        </span>
      </template>

      <!-- Columna de cliente -->
      <template v-slot:item.cliente="{ item }">
        <div>
          <div class="font-weight-medium">{{ item.cliente?.nombre || 'Cliente no encontrado' }}</div>
          <div class="text-caption text-grey">{{ item.ci_cliente }}</div>
        </div>
      </template>

      <!-- Columna de fecha de crédito -->
      <template v-slot:item.fecha_credito_formatted="{ item }">
        <div>
          <div class="font-weight-medium">{{ item.fecha_credito_formatted }}</div>
          <div class="text-caption text-grey">
            {{ item.dias_desde_credito }} días
          </div>
        </div>
      </template>

      <!-- Columna de monto total -->
      <template v-slot:item.monto_total="{ item }">
        <span class="font-weight-medium">
          {{ formatCurrency(item.monto_total) }}
        </span>
      </template>

      <!-- Columna de monto pagado -->
      <template v-slot:item.monto_pagado="{ item }">
        <div>
          <span class="font-weight-medium text-success">
            {{ formatCurrency(item.monto_pagado) }}
          </span>
          <v-progress-linear
            :model-value="item.porcentaje_pagado"
            color="success"
            height="4"
            class="mt-1"
          />
          <div class="text-caption">{{ item.porcentaje_pagado }}%</div>
        </div>
      </template>

      <!-- Columna de monto pendiente -->
      <template v-slot:item.monto_pendiente="{ item }">
        <span class="font-weight-medium text-error">
          {{ formatCurrency(item.monto_pendiente) }}
        </span>
      </template>

      <!-- Columna de estado -->
      <template v-slot:item.estado="{ item }">
        <v-chip
          :color="getStatusColor(item.estado)"
          variant="tonal"
          size="small"
        >
          <v-icon start>{{ getStatusIcon(item.estado) }}</v-icon>
          {{ item.estado }}
        </v-chip>
      </template>

      <!-- Columna de último abono -->
      <template v-slot:item.fecha_ultimo_abono_formatted="{ item }">
        <div v-if="item.fecha_ultimo_abono">
          <div class="font-weight-medium">{{ item.fecha_ultimo_abono_formatted }}</div>
        </div>
        <v-chip v-else color="grey" variant="tonal" size="small">
          <v-icon start>mdi-calendar-remove</v-icon>
          Sin abonos
        </v-chip>
      </template>

      <!-- Columna de acciones -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex gap-1">
          <v-tooltip text="Registrar pago">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-cash-plus"
                size="small"
                color="success"
                variant="tonal"
                :disabled="item.estado === 'Pagado'"
                @click="makePayment(item)"
              />
            </template>
          </v-tooltip>

          <v-tooltip text="Ver detalles">
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
        </div>
      </template>

      <!-- Template cuando no hay datos -->
      <template v-slot:no-data>
        <div class="text-center pa-4">
          <v-icon size="48" color="grey-lighten-1" class="mb-4">
            mdi-account-credit-card-outline
          </v-icon>
          <div class="text-h6 mb-2">No hay créditos registrados</div>
          <div class="text-subtitle-1 text-grey">
            Los créditos aparecerán aquí cuando se registren en el sistema.
          </div>
        </div>
      </template>
    </v-data-table>

    <!-- Botón de actualizar lista -->
    <ReloadButton :loading="loading" @click="$emit('refresh')" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import ReloadButton from '@/components/common/ReloadButton.vue';

const props = defineProps({
  creditos: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['refresh', 'make-payment', 'view-details']);

// Headers para la tabla
const headers = [
  { title: 'ID Crédito', key: 'id_credito', sortable: true },
  { title: 'Cliente', key: 'cliente', sortable: false },
  { title: 'Fecha Crédito', key: 'fecha_credito_formatted', sortable: true },
  { title: 'Monto Total', key: 'monto_total', sortable: true },
  { title: 'Pagado', key: 'monto_pagado', sortable: true },
  { title: 'Pendiente', key: 'monto_pendiente', sortable: true },
  { title: 'Estado', key: 'estado', sortable: true },
  { title: 'Último Abono', key: 'fecha_ultimo_abono_formatted', sortable: true },
  { title: 'Acciones', key: 'actions', sortable: false, width: '120px' }
];

// Computadas para métricas
const totalAdeudado = computed(() => {
  return props.creditos
    .filter(credito => credito.estado !== 'Pagado')
    .reduce((total, credito) => total + credito.monto_pendiente, 0);
});

const totalPagado = computed(() => {
  return props.creditos.reduce((total, credito) => total + credito.monto_pagado, 0);
});

const clientesConDeuda = computed(() => {
  const clientesUnicos = new Set(
    props.creditos
      .filter(credito => credito.estado !== 'Pagado')
      .map(credito => credito.ci_cliente)
  );
  return clientesUnicos.size;
});

// Funciones de formato
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(amount);
}

function getStatusColor(estado) {
  const colors = {
    'Pagado': 'success',
    'Pendiente': 'error',
    'Parcial': 'warning'
  };
  return colors[estado] || 'grey';
}

function getStatusIcon(estado) {
  const icons = {
    'Pagado': 'mdi-check-circle',
    'Pendiente': 'mdi-clock-alert',
    'Parcial': 'mdi-progress-clock'
  };
  return icons[estado] || 'mdi-help-circle';
}

function makePayment(creditData) {
  emit('make-payment', creditData);
}

function viewDetails(creditData) {
  emit('view-details', creditData);
}
</script>

<style scoped>
.debt-list {
  width: 100%;
}
</style>