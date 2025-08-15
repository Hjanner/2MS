<script setup>
import { ref, onMounted, computed } from 'vue';
import { useApiErrorHandler } from '@/composables/useApiErrorHandler';
import { useSnackbar } from '@/composables/useSnackbar';
import PaymentsList from '@/components/payments/PaymentsList.vue';
import PaymentsDetail from '@/components/payments/PaymentsDetail.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import { getFirstAndLastDayOfMonth } from '@/utils/formatters.js';
import { MONTH_NAMES } from '@/api/data.js';
import api from '@/api/api.js';

const pagos = ref([]);
const filteredPagos = ref([]);
const loading = ref(false);
const showDetailModal = ref(false);
const currentPayment = ref(null);
const currentMonth = ref('');

const { handleApiError } = useApiErrorHandler();
const { showSnackbar } = useSnackbar();

async function fetchPagos() {
  loading.value = true;
  try {
    const { firstDay, lastDay } = getFirstAndLastDayOfMonth();
        
    const response = await api.get('/pagos/listar/', {
      params: {
        fecha_inicio: firstDay,
        fecha_fin: lastDay,
        field_key: 'fecha_pago',
        order_field: 'fecha_pago',
        order_direction: 'DESC'
      }
    });
    
    pagos.value = response.data;

    const now = new Date();
    currentMonth.value = `${MONTH_NAMES[now.getMonth()]} ${now.getFullYear()}`;
    
  } catch (error) {
    handleApiError(error);
  } finally { 
    loading.value = false;
  }
}

function handleViewDetails(payment) {
  currentPayment.value = payment;
  showDetailModal.value = true;
}

function handleFilteredData(filtered) {
  filteredPagos.value = filtered;
}

// Calcular estadísticas de los pagos
const paymentStats = computed(() => {
  if (!filteredPagos.value || filteredPagos.value.length === 0) {
    return {
      totalPayments: 0,
      totalAmount: 0,
      byMethod: {},
      byCurrency: { bs: 0, usd: 0 }
    };
  }

  const stats = {
    totalPayments: filteredPagos.value.length,
    totalAmount: 0,
    byMethod: {},
    byCurrency: { bs: 0, usd: 0 }
  };

  filteredPagos.value.forEach(payment => {
    stats.totalAmount += payment.monto;
    
    // Agrupar por método de pago
    if (!stats.byMethod[payment.metodo_pago]) {
      stats.byMethod[payment.metodo_pago] = { count: 0, amount: 0 };
    }
    stats.byMethod[payment.metodo_pago].count += 1;
    stats.byMethod[payment.metodo_pago].amount += payment.monto;

    // Agrupar por moneda (basado en el método de pago)
    if (payment.metodo_pago === 'efectivo_usd') {
      stats.byCurrency.usd += payment.monto;
    } else {
      stats.byCurrency.bs += payment.monto;
    }
  });

  return stats;
});

onMounted(() => {
  fetchPagos();
});
</script>

<template>
  <div class="payments-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div class="d-flex align-center">
                <v-icon class="me-2">mdi-credit-card-multiple</v-icon>
                <span>Pagos Registrados - {{ currentMonth }}</span>
              </div>
            </v-card-title>
            
            <v-card-text>
                <!-- Información del mes actual -->
                <v-alert
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  <template #prepend>
                    <v-icon>mdi-calendar-month</v-icon>
                  </template>
                  Mostrando pagos del mes de <strong>{{ currentMonth }}</strong>
                </v-alert>

                <!-- Estadísticas resumidas -->
                <v-row class="mb-4" v-if="!loading && pagos.length > 0">
                  <v-col cols="12" sm="6" md="3">
                    <v-card color="primary" variant="tonal">
                      <v-card-text class="text-center">
                        <v-icon size="large" class="mb-2">mdi-credit-card-multiple</v-icon>
                        <div class="text-h4 font-weight-bold">{{ paymentStats.totalPayments }}</div>
                        <div class="text-subtitle-2">Total Pagos</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-card color="success" variant="tonal">
                      <v-card-text class="text-center">
                        <v-icon size="large" class="mb-2">mdi-currency-usd</v-icon>
                        <div class="text-h6 font-weight-bold">${{ paymentStats.byCurrency.usd.toFixed(2) }}</div>
                        <div class="text-subtitle-2">Total USD</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-card color="warning" variant="tonal">
                      <v-card-text class="text-center">
                        <v-icon size="large" class="mb-2">mdi-cash</v-icon>
                        <div class="text-h6 font-weight-bold">{{ paymentStats.byCurrency.bs.toLocaleString('es-VE') }} BS</div>
                        <div class="text-subtitle-2">Total Bolívares</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" sm="6" md="3">
                    <v-card color="info" variant="tonal">
                      <v-card-text class="text-center">
                        <v-icon size="large" class="mb-2">mdi-calculator</v-icon>
                        <div class="text-h6 font-weight-bold">{{ paymentStats.totalAmount.toLocaleString('es-VE') }}</div>
                        <div class="text-subtitle-2">Monto Total</div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <SearchFilter
                  :data="pagos"
                  :search-fields="['id_pago', 'id_venta', 'metodo_pago', 'referencia', 'num_tefl']"
                  placeholder="Buscar pagos por ID, venta, método, referencia o teléfono..."
                  :show-field-filter="true"
                  result-text="pagos"
                  @filtered="handleFilteredData"
                />

                <payments-list 
                  :pagos="filteredPagos" 
                  :loading="loading"
                  @refresh="fetchPagos"
                  @view-details="handleViewDetails"
                />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <PaymentsDetail
      v-model:show="showDetailModal"
      :payment-data="currentPayment"
      title="Detalles del Pago"
    />
  </div>
</template>

<style scoped>
.payments-page {
  padding: 20px 0;
}
</style>