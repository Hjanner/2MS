<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import SaleList from '@/components/sale/SaleList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import api from '@/api/api';
import {getFirstAndLastDayOfMonth} from '@/utils/formatters.js';

const { firstDay, lastDay } = getFirstAndLastDayOfMonth();
const ventas = ref([]);
const filteredVentas = ref([]);
const loading = ref(false);
const { showSnackbar } = useSnackbar();

async function fetchSales() {
  loading.value = true;
  try {
    // Usar el endpoint correcto con parámetros opcionales
    const response = await api.get('/ventas/listar/', {
      params: {
        fecha_inicio: firstDay,
        fecha_fin: lastDay,
        limit: 100
      }
    });
    ventas.value = response.data;
    filteredVentas.value = ventas.value;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar las ventas';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

function handleViewDetails(venta) {
  // Aquí implementaremos la navegación al detalle o apertura del modal
  console.log('Ver detalles de venta:', venta.venta.id_venta);
  // TODO: Implementar navegación o modal de detalles
  // Ejemplo: router.push(`/ventas/${venta.venta.id_venta}`)
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredVentas.value = filtered;
}

// Función para refrescar datos
function handleRefresh() {
  fetchSales();
}

onMounted(async () => {
  await fetchSales();
});
</script>

<template>
  <div class="sales-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Ventas</span>
              </div>
            </v-card-title>
            
            <v-card-text>
              <!-- Componente de búsqueda -->
              <SearchFilter
                :data="ventas"
                :search-fields="['venta.id_venta', 'venta.monto_total_usd', 'venta.monto_total_bs', 'venta.tipo', 'fecha_formateada', 'pago.metodo_pago', 'cliente.nombre', 'cliente.ci_cliente']"
                placeholder="Buscar por ID, monto, tipo, fecha, método de pago o cliente..."
                :show-field-filter="true"
                result-text="ventas"
                @filtered="handleFilteredData"
              />

              <SaleList 
                :ventas="filteredVentas" 
                :loading="loading"
                @refresh="handleRefresh"
                @view-details="handleViewDetails"  
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container> 
  </div>
</template>

<style scoped>
.sales-page {
  min-height: 100vh;
}
</style>