<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import ComprasList from '@/components/purchase/PurchasesList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import PurchaseForm from '@/components/purchase/PurchaseForm.vue';
import api from '@/api/api';
import { getCurrentDate, getCurrentTimeStamp } from '@/utils/formatters';

const compras = ref([]);
const filteredCompras = ref([]);
const loading = ref(false);
const addingCompra = ref(false);
const showAddDialog = ref(false);
const addCompraErrors = ref({});
const proveedores = ref([]);
const productos = ref([]);

// Fetch proveedores para el formulario
async function fetchProveedores() {
  try {
    const response = await api.get('/proveedores/');
    proveedores.value = response.data;
  } catch (error) {
    showSnackbar('Error al cargar proveedores', 'error');
  }
}

// Fetch productos no preparados para el formulario
async function fetchProductos() {
  try {
    const response = await api.get('/vista/productos-completos');
    // Filtrar solo productos no preparados
    productos.value = response.data.filter(producto => 
      producto.tipo_producto === 'noPreparado'
    );
  } catch (error) {
    showSnackbar('Error al cargar productos', 'error');
  }
}

// Fetch compras principales
async function fetchCompras() {
  loading.value = true;
  try {
    const response = await api.get('/compras/');    
    compras.value = response.data.map(compra => ({
      ...compra,
      fecha_formatted: new Date(compra.fecha).toLocaleDateString('es-ES'),
      proveedor_nombre: compra.Rif || 'Sin proveedor'
    }));
    filteredCompras.value = compras.value;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar las compras';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

async function addMovimiento(productData, id_currentCompra) {
    try {
        const movimientoPayload = {
            cod_producto: productData.cod_producto,
            referencia: 'compra',
            tipo_movimiento: 'entrada',
            cant_movida: productData.cantidad,
            costo_unitario: productData.costo_unitario,
            fc_actualizacion: getCurrentDate(),
            id_compra: id_currentCompra
        };
        await api.post('/movimientos', movimientoPayload);
    } catch (error) {
        const message = error.response?.data?.message || 'Error al agregar el producto';
        showSnackbar(message, 'error');
    }
}

// Manejar agregar nueva compra
async function handleAddCompra(compraData) {
  addingCompra.value = true;
  addCompraErrors.value = {};
  const productosCompra = compraData.productos;
  const id_currentCompra = getCurrentTimeStamp();
  
  try {
    const compraPayload = {
        id_compra: id_currentCompra || null,
        fecha: compraData.fecha,
        Rif: compraData.Rif,
        gasto_total: compraData.gasto_total,
    };

    await api.post('/compras/', compraPayload);        
    productosCompra.forEach(producto => {
        addMovimiento(producto, id_currentCompra);
    });
    await fetchCompras();
    showAddDialog.value = false;
    showSnackbar('Compra registrada correctamente', 'success');
  } catch (error) {
    handleApiError(error, addCompraErrors);
  } finally {
    addingCompra.value = false;
  }
}

// Función auxiliar para manejar errores de API
function handleApiError(error, errorRef) {
  console.log('Error de API:', error);
  
  if (error.response) {
    const backendErrors = {};

    if (error.response?.data?.detail) {
      const errorDetail = error.response.data.detail;

      if (Array.isArray(errorDetail)) {
        // Múltiples errores de validación
        errorDetail.forEach(err => {
          if (err.loc && err.loc.length > 1) {
            backendErrors[err.loc[1]] = err.msg;
          }
        });
      } else if (typeof errorDetail === 'object' && errorDetail.field) {
        // Error de campo específico
        backendErrors[errorDetail.field] = errorDetail.message;
      } else if (typeof errorDetail === 'string') {
        // Error general
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
  filteredCompras.value = filtered;
}

// Función para refrescar datos
function handleRefresh() {
  fetchCompras();
}

// Cerrar diálogos y limpiar errores
function closeAddDialog() {
  showAddDialog.value = false;
  addCompraErrors.value = {};
}

onMounted(async () => {
  await fetchProveedores();
  await fetchProductos();
  await fetchCompras();    
});
</script>

<template>
  <div class="compras-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Compras</span>
              </div>

              <v-btn
                color="primary"
                @click="showAddDialog = true"
              >
                <v-icon left>mdi-plus</v-icon>
                Registrar Compra
              </v-btn>
            </v-card-title>
            
            <v-card-text>
              <!-- Componente de búsqueda -->
              <SearchFilter
                :data="compras"
                :search-fields="['id_compra', 'fecha', 'razon_social', 'gasto_total']"
                placeholder="Buscar por ID, fecha, proveedor o monto..."
                :show-field-filter="true"
                result-text="compras"
                @filtered="handleFilteredData"
              />

              <ComprasList 
                :compras="filteredCompras" 
                :loading="loading"
                :proveedores="proveedores"  
                @refresh="handleRefresh"
                @edit="handleEditClick"  
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container> 
  </div>

  <!-- Add Compra Dialog -->
  <PurchaseForm
    v-model:show="showAddDialog"
    :loading="addingCompra"
    title="Registrar Nueva Compra"
    :proveedores="proveedores"
    :productos="productos"
    :errors="addCompraErrors"
    mode="add"
    @submit="handleAddCompra"
    @update:show="closeAddDialog"
  />
</template>

<style scoped>
.compras-page {
  padding: 20px 0;
}
</style>

<!-- si algun dia queremos implementar edicion -->
  <!-- // Manejar editar compra
// async function handleEditCompra(compraData) {
//   editingCompra.value = true;
//   editCompraErrors.value = {};
  
//   try {
//     const compraPayload = {
//       fecha: compraData.fecha,
//       Rif: compraData.Rif,
//       gasto_total: compraData.gasto_total,
//       productos: compraData.productos
//     };

//     await api.put(`/compras/${currentCompra.value.id_compra}`, compraPayload);
//     await fetchCompras();
//     showEditDialog.value = false;
//     currentCompra.value = null;
//     showSnackbar('Compra editada correctamente', 'success');
//   } catch (error) {
//     handleApiError(error, editCompraErrors);
//   } finally {
//     editingCompra.value = false;
//   }
// }

// // Manejar click de editar
// function handleEditClick(compra) {
//   currentCompra.value = compra;
//   showEditDialog.value = true;
// } -->

  <!-- Edit Compra Dialog -->
  <!-- <PurchaseForm
    v-model:show="showEditDialog"
    :loading="editingCompra"
    :compra-data="currentCompra"
    :proveedores="proveedores"
    :productos="productos"
    title="Editar Compra"
    :errors="editCompraErrors"
    mode="edit"
    @submit="handleEditCompra"
    @update:show="closeEditDialog"
  />       -->