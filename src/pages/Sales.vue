
<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import SaleList from '@/components/sale/SaleList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import api from '@/api/api';

const ventas = ref([]);
const filteredVentas = ref([]);
const loading = ref(false);
const { showSnackbar } = useSnackbar();

async function fetchSales() {
  loading.value = true;
  try {
    const response = await api.get('/ventas');    
    // Asumo que el endpoint retorna una lista de ResumenVenta
    ventas.value = response.data;    
        console.log(ventas);

    filteredVentas.value = ventas.value;
    console.log('primera vuelta se envia', filteredVentas.value);
    
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
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredVentas.value = filtered;
  if (filtered.length === 0) {
    showSnackbar('No se encontraron resultados', 'info');
  } else {
    showSnackbar(`Se encontraron ${filtered.length} resultados`, 'success');
  }
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
                :search-fields="['id_venta', 'monto_total_usd', 'monto_total_bs', 'tipo', 'fecha_formateada', 'metodo_pago']"
                placeholder="Buscar por ID, monto, tipo, fecha o método de pago..."
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