<script setup>
import { ref, onMounted } from 'vue';
import { useApiErrorHandler } from '@/composables/useApiErrorHandler';
import { useSnackbar } from '@/composables/useSnackbar';
import ExchangeRateList from '@/components/exchange/ExchangeRateList.vue';
import ExchangeRateForm from '@/components/exchange/ExchangeRateForm.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import { getFirstAndLastDayOfMonth } from '@/utils/formatters.js';
import api from '@/api/api.js';

const tasasCambio = ref([]);
const filteredTasasCambio = ref([]);
const loading = ref(false);
const showExchangeRateForm = ref(false);
const formLoading = ref(false);
const formErrors = ref({});
const currentMonth = ref('');

const { handleApiError, handleSuccess } = useApiErrorHandler();
const { showSnackbar } = useSnackbar();

async function fetchTasasCambio() {
  loading.value = true;
  try {
    const { firstDay, lastDay } = getFirstAndLastDayOfMonth();    
    
    const response = await api.get('/tasas_cambio/listar/', {
      params: {
        fecha_inicio: firstDay,
        fecha_fin: lastDay
      }
    });
    
    tasasCambio.value = response.data;
    
    // Establecer el mes actual para mostrar en la interfaz
    const monthNames = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    const now = new Date();
    currentMonth.value = `${monthNames[now.getMonth()]} ${now.getFullYear()}`;
    
  } catch (error) {
    handleApiError(error);
  } finally { 
    loading.value = false;
  }
}

async function handleSubmit(exchangeRateData) {
  formLoading.value = true;
  formErrors.value = {};
  
  try {
    // Solo crear tasas manuales, no hay edición
    await api.post('/tasas_cambio', exchangeRateData);
    handleSuccess('Tasa de cambio creada correctamente');
    
    showExchangeRateForm.value = false;
    await fetchTasasCambio();
  } catch (error) {
    handleApiError(error, formErrors);
  } finally {
    formLoading.value = false;
  }
}

function handleAddExchangeRate() {
  showExchangeRateForm.value = true;
}

function handleFilteredData(filtered) {
  filteredTasasCambio.value = filtered;
}

onMounted(() => {
  fetchTasasCambio();
});
</script>

<template>
  <div class="exchange-rates-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div class="d-flex align-center">
                <v-icon class="me-2">mdi-currency-usd</v-icon>
                <span>Tasas de Cambio - {{ currentMonth }}</span>
              </div>
              <v-btn 
                color="primary"
                @click="handleAddExchangeRate"
              >
                <v-icon left>mdi-plus</v-icon>
                Nueva Tasa Manual
              </v-btn>
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
                  Mostrando tasas de cambio del mes de <strong>{{ currentMonth }}</strong>
                </v-alert>

                <SearchFilter
                  :data="tasasCambio"
                  :search-fields="['origen', 'fecha']"
                  placeholder="Buscar tasas por origen o fecha..."
                  :show-field-filter="true"
                  result-text="tasas de cambio"
                  @filtered="handleFilteredData"
                />

                <exchange-rate-list 
                  :tasas-cambio="filteredTasasCambio" 
                  :loading="loading"
                  @refresh="fetchTasasCambio"
                />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <ExchangeRateForm
      v-model:show="showExchangeRateForm"
      title="Agregar Tasa de Cambio Manual"
      :loading="formLoading"
      :errors="formErrors"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped>
.exchange-rates-page {
  padding: 20px 0;
}
</style>