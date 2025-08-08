<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import InventoryList from '@/components/inventory/InventoryList.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/common/BacktoHome.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import api from '@/api/api';

const productos = ref([]);
const filteredProductos = ref([]);
const loading = ref(false);
const { showSnackbar } = useSnackbar();
const addingProduct = ref(false);
const showAddDialog = ref(false);
const addProductErrors = ref({});
const categorias = ref([]);
const editingProduct = ref(false);
const showEditDialog = ref(false);
const editProductErrors = ref({});
const currentProduct = ref(null);


async function fetchCategorias() {
  try {
    const response = await api.get('/categoria_productos');
    categorias.value = response.data;
  } catch (error) {
    showSnackbar('Error al cargar categorías', 'error');
  }
}

async function fetchProducts() {
  loading.value = true;
  try {
    const response = await api.get('/vista/productos-completos');
    productos.value = response.data.map(producto => ({
      ...producto,
      nombre_categoria: producto.categoria_descr
    }));
    filteredProductos.value = productos.value;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar los productos';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

async function handleAddProduct(productData) {
  addingProduct.value = true;
  addProductErrors.value = {};
  try {
    let endpointTipo;
    let productoBase;
    let productoTipo;

    // Determinar endpoint según el tipo de producto
    if (productData.tipo_producto === 'noPreparado') {
      endpointTipo = '/productos_noPreparados';
      productoBase = {
        cod_producto: productData.cod_producto,
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
      };
      productoTipo = {
        cod_producto_noPreparado: productData.cod_producto,
        cant_min: productData.cant_min,
        cant_actual: productData.cant_actual,
        costo_compra: productData.costo_compra,
        unidad_medida: productData.unidad_medida,
        Rif: productData.Rif || null
      };
    } else {
      endpointTipo = '/productos_preparados';
      productoBase = {
        cod_producto: productData.cod_producto,
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
      };
      productoTipo = {
        cod_producto_preparado: productData.cod_producto,
        descr: productData.descr || null
      };
    }

    await api.post('/productos', productoBase);
    await api.post(endpointTipo, productoTipo);
    await fetchProducts();
    showAddDialog.value = false;
    showSnackbar(`Producto ${productData.tipo_producto === 'noPreparado' ? 'no preparado' : 'preparado'} agregado correctamente`, 'success');
  } catch (error) {
    handleApiError(error, addProductErrors);
  } finally {
    addingProduct.value = false;
  }
}

async function handlerEditProduct(productData) {
  editingProduct.value = true;
  editProductErrors.value = {};
  
  try {
    let endpointTipo;
    let productoBase;
    let productoTipo;


    // Determinar endpoint según el tipo de producto
    if (productData.tipo_producto === 'noPreparado') {
      endpointTipo = `/productos_noPreparados/${currentProduct.value.cod_producto}`;
      productoBase = {
        cod_producto: productData.cod_producto,
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
      };
      productoTipo = {
        cod_producto_noPreparado: productData.cod_producto,
        cant_min: productData.cant_min,
        cant_actual: productData.cant_actual,
        costo_compra: productData.costo_compra,
        unidad_medida: productData.unidad_medida,
        Rif: productData.Rif || null
      };
    } else {
      endpointTipo = `/productos_preparados/${currentProduct.value.cod_producto}`;
      productoBase = {
        cod_producto: productData.cod_producto,
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
      };
      productoTipo = {
        cod_producto_preparado: productData.cod_producto,
        descr: productData.descr || null
      };
    }

    await api.put(`/productos/${currentProduct.value.cod_producto}`, productoBase);
    await api.put(endpointTipo, productoTipo);
    await fetchProducts();
    showEditDialog.value = false;
    currentProduct.value = null;
    showSnackbar(`Producto ${productData.tipo_producto === 'noPreparado' ? 'no preparado' : 'preparado'} editado correctamente`, 'success');
  } catch (error) {
    handleApiError(error, editProductErrors);
  } finally {
    editingProduct.value = false;
  }
}

function handleEditClick(producto) {
  currentProduct.value = producto;
  showEditDialog.value = true;
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
  filteredProductos.value = filtered;
}

// Función para refrescar datos
function handleRefresh() {
  fetchProducts();
}

// Cerrar diálogos y limpiar errores
function closeAddDialog() {
  showAddDialog.value = false;
  addProductErrors.value = {};
}

function closeEditDialog() {
  showEditDialog.value = false;
  editProductErrors.value = {};
  currentProduct.value = null;
}

onMounted(async () => {
  await fetchCategorias();
  await fetchProducts();
});
</script>

<template>
  <div class="inventory-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Inventario</span>
              </div>

              <v-btn
                color="primary"
                @click="showAddDialog = true"
              >
                <v-icon left>mdi-plus</v-icon>
                Agregar Producto
              </v-btn>
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
                :categorias="categorias"  
                @refresh="handleRefresh"
                @edit="handleEditClick"  
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container> 
  </div>

    <!-- Add Product Dialog -->
    <ProductForm
      v-model:show="showAddDialog"
      :loading="addingProduct"
      title="Agregar Nuevo Producto"
      :categorias="categorias"
      :errors="addProductErrors"
      mode="add"
      @submit="handleAddProduct"
      @update:show="closeAddDialog"
    />

    <!-- Edit Product Dialog -->
    <ProductForm
      v-model:show="showEditDialog"
      :loading="editingProduct"
      :product-data="currentProduct"
      :categorias="categorias"
      title="Editar Producto"
      :errors="editProductErrors"
      mode="edit"
      @submit="handlerEditProduct"
      @update:show="closeEditDialog"
    />      
</template>

<style scoped>
.inventory-page {
  padding: 20px 0;
}
</style>