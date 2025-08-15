<script>
import ReloadButton from '@/components/common/ReloadButton.vue';

export default {
  name: 'PaymentsList',
  props: {
    pagos: {
      type: Array,
      required: true,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      headers: [
        { title: 'ID Pago', key: 'id_pago', sortable: true, width: '100px' },
        { title: 'ID Venta', key: 'id_venta', sortable: true, width: '100px' },
        { title: 'Monto', key: 'monto', sortable: true, width: '150px' },
        { title: 'Fecha', key: 'fecha_pago', sortable: true, width: '130px' },
        { title: 'Método', key: 'metodo_pago', sortable: true, width: '150px' },
        { title: 'Referencia', key: 'referencia', sortable: false, width: '150px' },
        { title: 'Teléfono', key: 'num_tefl', sortable: false, width: '130px' },
        { title: 'Acciones', key: 'actions', sortable: false, width: '100px' },
      ],
      metodoPagoConfig: {
        'efectivo_bs': { 
          label: 'Efectivo BS', 
          color: 'success', 
          icon: 'mdi-cash',
          currency: 'BS'
        },
        'efectivo_usd': { 
          label: 'Efectivo USD', 
          color: 'green-darken-2', 
          icon: 'mdi-currency-usd',
          currency: 'USD'
        },
        'pago_movil': { 
          label: 'Pago Móvil', 
          color: 'primary', 
          icon: 'mdi-cellphone',
          currency: 'BS'
        },
        'debito': { 
          label: 'Débito', 
          color: 'orange', 
          icon: 'mdi-credit-card',
          currency: 'BS'
        },
        'transferencia': { 
          label: 'Transferencia', 
          color: 'purple', 
          icon: 'mdi-bank-transfer',
          currency: 'BS'
        }
      }
    };
  },
  methods: {
    formatFecha(fecha) {
      if (!fecha) return 'No especificado';
      
      try {
        const date = new Date(fecha);
        return date.toLocaleDateString('es-VE', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      } catch (error) {
        return fecha;
      }
    },
    
    formatMonto(monto, metodo) {
      if (!monto) return 'N/A';
      
      try {
        const number = parseFloat(monto);
        const config = this.metodoPagoConfig[metodo];
        
        if (config?.currency === 'USD') {
          return `$${number.toFixed(2)}`;
        } else {
          return `${number.toLocaleString('es-VE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          })} BS`;
        }
      } catch (error) {
        return monto;
      }
    },

    getMetodoConfig(metodo) {
      return this.metodoPagoConfig[metodo] || {
        label: metodo,
        color: 'default',
        icon: 'mdi-help-circle',
        currency: 'BS'
      };
    },

    isRecentPayment(fecha) {
      if (!fecha) return false;
      const paymentDate = new Date(fecha);
      const now = new Date();
      const diffHours = (now - paymentDate) / (1000 * 60 * 60);
      return diffHours <= 24; // Últimas 24 horas
    },

    formatReferencia(referencia) {
      if (!referencia) return 'Sin referencia';
      // Limitar longitud para mejor visualización
      return referencia.length > 15 ? `${referencia.substring(0, 15)}...` : referencia;
    },

    formatTelefono(telefono) {
      if (!telefono) return 'N/A';
      // Formatear número de teléfono venezolano
      if (telefono.length === 11) {
        return `${telefono.substring(0, 4)}-${telefono.substring(4, 7)}-${telefono.substring(7)}`;
      }
      return telefono;
    }
  },
  emits: ['refresh', 'view-details']
};
</script>

<template>
  <div class="payments-list">
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-4"
    ></v-progress-linear>

    <v-alert
      v-if="!loading && pagos.length === 0"
      type="info"
      class="mb-4"
    >
      <template #prepend>
        <v-icon>mdi-information-outline</v-icon>
      </template>
      No se encontraron pagos para este mes.
    </v-alert>

    <!-- render de lista de datos -->
    <v-data-table 
      :headers="headers"
      :items="pagos"
      :loading="loading"
      item-key="id_pago"
      class="elevation-1"
      :sort-by="[{ key: 'fecha_pago', order: 'desc' }]"
    >
      <!-- Formatear columna de ID Pago -->
      <template v-slot:item.id_pago="{ item }">
        <v-chip
          size="small"
          color="primary"
          variant="outlined"
        >
          #{{ item.id_pago }}
        </v-chip>
      </template>

      <!-- Formatear columna de ID Venta -->
      <template v-slot:item.id_venta="{ item }">
        <v-chip
          size="small"
          color="secondary"
          variant="tonal"
        >
          V{{ item.id_venta }}
        </v-chip>
      </template>

      <!-- Formatear columna de monto -->
      <template v-slot:item.monto="{ item }">
        <div class="d-flex align-center">
          <v-chip
            :color="getMetodoConfig(item.metodo_pago).currency === 'USD' ? 'green-darken-2' : 'success'"
            variant="tonal"
            size="small"
            class="font-weight-bold"
          >
            {{ formatMonto(item.monto, item.metodo_pago) }}
          </v-chip>
        </div>
      </template>

      <!-- Formatear columna de fecha -->
      <template v-slot:item.fecha_pago="{ item }">
        <div class="d-flex flex-column">
          <span class="text-body-2">{{ formatFecha(item.fecha_pago) }}</span>
          <!-- <v-chip
            v-if="isRecentPayment(item.fecha_pago)"
            size="x-small"
            color="success"
            variant="tonal"
            class="mt-1"
          >
            <v-icon start size="x-small">mdi-clock-fast</v-icon>
            Reciente
          </v-chip> -->
        </div>
      </template>

      <!-- Formatear columna de método de pago -->
      <template v-slot:item.metodo_pago="{ item }">
        <v-chip
          :color="getMetodoConfig(item.metodo_pago).color"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ getMetodoConfig(item.metodo_pago).icon }}
          </v-icon>
          {{ getMetodoConfig(item.metodo_pago).label }}
        </v-chip>
      </template>

      <!-- Formatear columna de referencia -->
      <template v-slot:item.referencia="{ item }">
        <div v-if="item.referencia">
          <v-tooltip :text="item.referencia">
            <template #activator="{ props }">
              <span v-bind="props" class="text-caption">
                {{ formatReferencia(item.referencia) }}
              </span>
            </template>
          </v-tooltip>
        </div>
        <span v-else class="text-medium-emphasis text-caption">Sin referencia</span>
      </template>

      <!-- Formatear columna de teléfono -->
      <template v-slot:item.num_tefl="{ item }">
        <span v-if="item.num_tefl" class="text-caption">
          {{ formatTelefono(item.num_tefl) }}
        </span>
        <span v-else class="text-medium-emphasis text-caption">N/A</span>
      </template>

      <!-- Botón de acciones (solo ver detalles) -->
      <template v-slot:item.actions="{ item }">
        <v-btn 
          icon 
          size="small" 
          color="primary" 
          @click="$emit('view-details', item)"
          variant="tonal"
        >
          <v-icon>mdi-eye-outline</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <!-- Información adicional -->
    <v-card 
      v-if="!loading && pagos.length > 0"
      variant="outlined" 
      class="mt-4"
    >
      <v-card-text>
        <v-row class="align-center">
          <v-col cols="12" md="6">
            <div class="d-flex align-center">
              <v-icon color="info" class="me-2">mdi-information</v-icon>
              <span class="text-body-2">
                Total de pagos este mes: <strong>{{ pagos.length }}</strong>
              </span>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="d-flex align-center justify-end gap-2">
              <v-chip 
                v-for="(config, method) in metodoPagoConfig" 
                :key="method"
                :color="config.color" 
                variant="tonal" 
                size="small"
              >
                <v-icon start>{{ config.icon }}</v-icon>
                {{ pagos.filter(p => p.metodo_pago === method).length }}
              </v-chip>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <ReloadButton @click="$emit('refresh')" />
  </div>
</template>

<style scoped>
.payments-list {
  width: 100%;
}
</style>