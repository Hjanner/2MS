<script>
import ReloadButton from '@/components/common/ReloadButton.vue';

export default {
  name: 'ExchangeRateList',
  props: {
    tasasCambio: {
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
        { title: 'ID', key: 'id_tasa', sortable: true, width: '80px' },
        { title: 'Fecha', key: 'fecha', sortable: true, width: '180px' },
        { title: 'Tasa (1 USD = X BS)', key: 'valor_usd_bs', sortable: true, width: '200px' },
        { title: 'Origen', key: 'origen', sortable: true, width: '150px' },
      ],
      origenColors: {
        'BCV': 'success',
        'Manual': 'primary'
      },
      origenIcons: {
        'BCV': 'mdi-bank',
        'Manual': 'mdi-account-edit'
      }
    };
  },
  methods: {
    formatFecha(fecha) {
      if (!fecha) return 'No especificado';
      
      try {
        const date = new Date(fecha);
        const options = {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        };
        return date.toLocaleDateString('es-VE', options);
      } catch (error) {
        return fecha;
      }
    },
    
    formatCurrency(value) {
      if (!value) return 'N/A';
      
      try {
        const number = parseFloat(value);
        return new Intl.NumberFormat('es-VE', {
          style: 'currency',
          currency: 'VES',
          minimumFractionDigits: 2,
          maximumFractionDigits: 4
        }).format(number);
      } catch (error) {
        return value;
      }
    },

    isRecentRate(fecha) {
      if (!fecha) return false;
      const rateDate = new Date(fecha);
      const now = new Date();
      const diffHours = (now - rateDate) / (1000 * 60 * 60);
      return diffHours <= 24; // Últimas 24 horas
    }
  },
  emits: ['refresh']
};
</script>

<template>
  <div class="exchange-rate-list">
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-4"
    ></v-progress-linear>

    <v-alert
      v-if="!loading && tasasCambio.length === 0"
      type="info"
      class="mb-4"
    >
      <template #prepend>
        <v-icon>mdi-information-outline</v-icon>
      </template>
      No se encontraron tasas de cambio para este mes. 
      Puede agregar una tasa manual usando el botón "Nueva Tasa Manual".
    </v-alert>

    <!-- render de lista de datos -->
    <v-data-table 
      :headers="headers"
      :items="tasasCambio"
      :loading="loading"
      item-key="id_tasa"
      class="elevation-1"
      :sort-by="[{ key: 'fecha', order: 'desc' }]"
    >
      <!-- Formatear columna de ID -->
      <template v-slot:item.id_tasa="{ item }">
        <v-chip
          size="small"
          color="primary"
          variant="outlined"
        >
          #{{ item.id_tasa }}
        </v-chip>
      </template>

      <!-- Formatear columna de fecha -->
      <template v-slot:item.fecha="{ item }">
        <div class="d-flex flex-column">
          <span class="text-body-2">{{ formatFecha(item.fecha) }}</span>
        </div>
      </template>

      <!-- Formatear columna de valor con énfasis -->
      <template v-slot:item.valor_usd_bs="{ item }">
        <div class="d-flex align-center">
          <v-chip
            color="success"
            variant="tonal"
            size="small"
            class="font-weight-bold"
          >
            <v-icon start size="small">mdi-currency-usd</v-icon>
            {{ formatCurrency(item.valor_usd_bs) }}
          </v-chip>
        </div>
      </template>

      <!-- Formatear columna de origen con chips de colores -->
      <template v-slot:item.origen="{ item }">
        <v-chip
          :color="origenColors[item.origen] || 'default'"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ origenIcons[item.origen] || 'mdi-help-circle' }}
          </v-icon>
          {{ item.origen }}
        </v-chip>
      </template>
    </v-data-table>
    
    <ReloadButton @click="$emit('refresh')" />
  </div>
</template>

<style scoped>
.exchange-rate-list {
  width: 100%;
}
</style>