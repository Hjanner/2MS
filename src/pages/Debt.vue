<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import DebtList from '@/components/debt/DebtList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
// import PaymentModal from '@/components/debt/PaymentModal.vue';
import api from '@/api/api';

const creditos = ref([]);
const filteredCreditos = ref([]);
const loading = ref(false);
const paymentModal = ref({
  show: false,
  creditId: null,
  creditData: null
});
const paymentLoading = ref(false);
const paymentErrors = ref({});
const { showSnackbar } = useSnackbar();

async function fetchDebts() {
  loading.value = true;
  try {
    const response = await api.get('/creditos/');
    
    // Formatear los datos para incluir información calculada
    creditos.value = response.data.map(credito => ({
      ...credito,
      monto_pendiente: credito.monto_total - credito.monto_pagado,
      porcentaje_pagado: credito.monto_total > 0 
        ? ((credito.monto_pagado / credito.monto_total) * 100).toFixed(1)
        : 0,
      dias_desde_credito: Math.floor((new Date() - new Date(credito.fecha_credito)) / (1000 * 60 * 60 * 24)),
      fecha_credito_formatted: new Date(credito.fecha_credito).toLocaleDateString('es-ES'),
      fecha_ultimo_abono_formatted: credito.fecha_ultimo_abono 
        ? new Date(credito.fecha_ultimo_abono).toLocaleDateString('es-ES')
        : 'Sin abonos'
    }));
    
    filteredCreditos.value = creditos.value;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar las deudas';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

function handleMakePayment(creditData) {
  paymentModal.value = {
    show: true,
    creditId: creditData.id_credito,
    creditData: creditData
  };
}

async function handleSubmitPayment(paymentData) {
  paymentLoading.value = true;
  paymentErrors.value = {};
  
  try {
    // Calcular nuevo monto pagado
    const nuevoMontoPagado = paymentModal.value.creditData.monto_pagado + paymentData.monto_abono;
    const montoTotal = paymentModal.value.creditData.monto_total;
    
    // Determinar nuevo estado
    let nuevoEstado = 'Parcial';
    if (nuevoMontoPagado >= montoTotal) {
      nuevoEstado = 'Pagado';
    } else if (nuevoMontoPagado === 0) {
      nuevoEstado = 'Pendiente';
    }
    
    // Actualizar el crédito
    const updateData = {
      monto_pagado: nuevoMontoPagado,
      fecha_ultimo_abono: paymentData.fecha_pago,
      estado: nuevoEstado
    };
    
    await api.put(`/creditos/${paymentModal.value.creditId}`, updateData);
    
    showSnackbar('Pago registrado correctamente', 'success');
    paymentModal.value.show = false;
    await fetchDebts(); // Recargar la lista
    
  } catch (error) {
    handleApiError(error, paymentErrors);
  } finally {
    paymentLoading.value = false;
  }
}

function handleViewDetails(creditData) {
  console.log('Ver detalles del crédito:', creditData.id_credito);
  // TODO: Implementar modal de detalles o navegación
}

// Función auxiliar para manejar errores de API
function handleApiError(error, errorRef) {
  console.log('Error de API:', error);
  
  if (error.response) {
    const backendErrors = {};

    if (error.response?.data?.detail) {
      const errorDetail = error.response.data.detail;

      if (Array.isArray(errorDetail)) {
        errorDetail.forEach(err => {
          if (err.loc && err.loc.length > 1) {
            backendErrors[err.loc[1]] = err.msg;
          }
        });
      } else if (typeof errorDetail === 'object' && errorDetail.field) {
        backendErrors[errorDetail.field] = errorDetail.message;
      } else if (typeof errorDetail === 'string') {
        backendErrors.general = errorDetail;
      }

      errorRef.value = backendErrors;
      const errorMessages = Object.values(backendErrors).join(', ');
      showSnackbar(errorMessages || 'Ocurrió un error inesperado.', 'error');
    } else {
      const message = error.response.data?.message || `Error del servidor: ${error.response.status}`;
      showSnackbar(message, 'error');
    }
  } else if (error.request) {
    console.log('Error de red:', error.request);
    showSnackbar('Error de conexión con el servidor', 'error');
  } else {
    console.log('Error:', error.message);
    showSnackbar('Error inesperado: ' + error.message, 'error');
  }
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredCreditos.value = filtered;
}

// Función para refrescar datos
function handleRefresh() {
  fetchDebts();
}

function closePaymentModal() {
  paymentModal.value.show = false;
  paymentErrors.value = {};
}

onMounted(async () => {
  await fetchDebts();
});
</script>

<template>
  <div class="debts-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Deudas</span>
                <div class="text-subtitle-1 text-grey">
                  Administra los créditos y pagos de clientes
                </div>
              </div>
            </v-card-title>
            
            <v-card-text>
              <!-- Componente de búsqueda -->
              <SearchFilter
                :data="creditos"
                :search-fields="[
                  'ci_cliente', 
                  'cliente.nombre', 
                  'monto_total', 
                  'monto_pagado', 
                  'monto_pendiente',
                  'estado',
                  'fecha_credito_formatted'
                ]"
                placeholder="Buscar por CI, nombre, monto, estado o fecha..."
                :show-field-filter="true"
                result-text="créditos"
                @filtered="handleFilteredData"
              />

              <DebtList 
                :creditos="filteredCreditos" 
                :loading="loading"
                @refresh="handleRefresh"
                @make-payment="handleMakePayment"
                @view-details="handleViewDetails"  
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Modal de Pago -->
    <PaymentModal
      v-model:show="paymentModal.show"
      :loading="paymentLoading"
      :credit-data="paymentModal.creditData"
      :errors="paymentErrors"
      @submit="handleSubmitPayment"
      @update:show="closePaymentModal"
    />
  </div>
</template>

<style scoped>
.debts-page {
  min-height: 100vh;
}
</style>