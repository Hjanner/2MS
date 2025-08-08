<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import InventoryList from '@/components/inventory/InventoryList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/common/BacktoHome.vue';
import api from '@/api/api';

const productos = ref([]);
const filteredProductos = ref([]);
const loading = ref(false);
const { showSnackbar } = useSnackbar();

// Separar productos por tipo
const productosNoPreparados = ref([]);
const productosPreparados = ref([]);

async function fetchInventory() {
  loading.value = true;
  try {
    const response = await api.get('/vista/productos-completos');
    productos.value = response.data;
    
    // Separar productos por tipo
    productosNoPreparados.value = response.data.filter(p => p.tipo_producto === 'noPreparado');
    productosPreparados.value = response.data.filter(p => p.tipo_producto === 'preparado');
    
    // Inicializar filtros con todos los productos
    filteredProductos.value = response.data;
    
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar el inventario';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredProductos.value = filtered;
}

// Función para refrescar datos
function handleRefresh() {
  fetchInventory();
}

onMounted(async () => {
  await fetchInventory();
});
</script>

<template>
  <div class="inventory-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <backto-home></backto-home>
          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Inventario</span>
                <div class="text-subtitle-1 mt-2">
                  <v-chip 
                    color="blue" 
                    variant="outlined" 
                    size="small" 
                    class="me-2"
                  >
                    <v-icon start>mdi-package-variant</v-icon>
                    No Preparados: {{ productosNoPreparados.length }}
                  </v-chip>
                  <v-chip 
                    color="orange" 
                    variant="outlined" 
                    size="small"
                  >
                    <v-icon start>mdi-chef-hat</v-icon>
                    Preparados: {{ productosPreparados.length }}
                  </v-chip>
                </div>
              </div>
            </v-card-title>
            
            <v-card-text>
              <!-- Componente de búsqueda -->
              <SearchFilter
                :data="productos"
                :search-fields="['nombre', 'categoria_descr', 'cod_producto', 'cant_actual', 'precio_usd']"
                placeholder="Buscar por nombre, categoría, código, cantidad o precio..."
                :show-field-filter="true"
                result-text="productos"
                @filtered="handleFilteredData"
              />

              <inventory-list 
                :productos="filteredProductos" 
                :loading="loading"
                @refresh="handleRefresh"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container> 
  </div>
</template>

<style scoped>
.inventory-page {
  padding: 20px 0;
}
</style>