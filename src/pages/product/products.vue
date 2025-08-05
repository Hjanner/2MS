<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import ProductList from '@/components/product/ProductList.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import ProductDelete from '@/components/product/ProductDelete.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/BacktoHome.vue';
import api from '@/api/api';

const productos = ref([]);
const filteredProductos = ref([]);
const loading = ref(false);
const addingProduct = ref(false);
const editingProduct = ref(false);
const deletingProduct = ref(false);
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDeleteDialog = ref(false);
const currentProduct = ref(null);
const { showSnackbar } = useSnackbar();
const addProductErrors = ref({});
const editProductErrors = ref({});

async function fetchProducts() {
  loading.value = true;
  try {
    const response = await api.get('/productos');
    productos.value = response.data;
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
    await api.post('/productos', productData);
    await fetchProducts();
    showAddDialog.value = false;
    showSnackbar('Producto agregado correctamente', 'success');
  } catch (error) {    
    if (error.response) {
      // console.log('Status:', error.response.status);
      // console.log('Data:', error.response.data);
      const backendErrors = {};

      if (error.response?.data?.detail) {
        const errorDetail = error.response.data.detail;

        if (Array.isArray(errorDetail)) {   // en caso de multiples errores
          errorDetail.forEach(err => {
            if (err.loc && err.loc.length > 1) {
              backendErrors[err.loc[1]] = err.msg;
              }
          });
        }
        else if (typeof errorDetail === 'object' && errorDetail.field) {
          backendErrors[errorDetail.field] = errorDetail.message;
        }

        addProductErrors.value = backendErrors;
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
  } finally {
    addingProduct.value = false;
  }
}

async function handlerEditProduct(productData) {
  editingProduct.value = true;
  editProductErrors.value = {};
  try {
    await api.put(`/productos/${currentProduct.value.cod_producto}`, productData);
    await fetchProducts();
    showEditDialog.value = false;
    currentProduct.value = null;
    showSnackbar('Producto editado correctamente', 'success');
  } catch (error) {
    console.log('este es el error que me da', error);
    
    if (error.response?.status === 422 && Array.isArray(error.response.data.detail)) {
      // Parse validation errors
      const backendErrors = {};
      for (const err of error.response.data.detail) {
        if (err.loc && err.loc.length > 1) {
          backendErrors[err.loc[1]] = err.msg;
        }
      }
      editProductErrors.value = backendErrors;
    } else {
      const message = error.response?.data?.message || 'Error al editar el producto';
      showSnackbar(message, 'error');
    }
  } finally {
    editingProduct.value = false;
  }
}

async function handlerDeleteProduct(cod_producto) {
  deletingProduct.value = true;
  try {
    await api.delete(`/productos/${cod_producto}`);
    await fetchProducts();
    showDeleteDialog.value = false;
    currentProduct.value = null;
    showSnackbar('Producto eliminado correctamente', 'success');
  } catch (error) {
    const message = error.response?.data?.message || 'Error al eliminar el producto';
    showSnackbar(message, 'error');
  } finally {
    deletingProduct.value = false;
  }
}

function handleEditClick(producto) {
  currentProduct.value = producto;
  showEditDialog.value = true;
}

function handleDeleteClick(producto) {    
  currentProduct.value = producto;  
  showDeleteDialog.value = true;
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredProductos.value = filtered;
}

// Opcional: manejar eventos de búsqueda para analytics o logs
// function handleSearch(searchData) {
//   console.log('Búsqueda realizada:', searchData);
// }

onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div class="products-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <backto-home></backto-home>
          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Gestión de Productos</span>
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
                  :search-fields="['cod_producto', 'nombre', 'precio', 'id_categoria']"
                  placeholder="Buscar productos por código, nombre, precio o categoría..."
                  :show-field-filter="true"
                  result-text="productos"
                  @filtered="handleFilteredData"
                  @search="handleSearch"
                />

                <product-list 
                  :productos="filteredProductos" 
                  :loading="loading"
                  @refresh="fetchProducts"
                  @edit="handleEditClick"
                  @delete="handleDeleteClick"
                />

            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Add Product Dialog -->
    <ProductForm
      v-model:show="showAddDialog"
      :loading="addingProduct"
      title="Agregar Nuevo Producto"
      :errors="addProductErrors"
      @submit="handleAddProduct"
      @update:show="(val) => { showAddDialog = val; if (!val) addProductErrors.value = {}; }"
    />

    <!-- Edit Product Dialog -->
    <ProductForm
      v-model:show="showEditDialog"
      :loading="editingProduct"
      :product-data="currentProduct"
      title="Editar Producto"
      :errors="editProductErrors"
      @submit="handlerEditProduct"
      @update:show="(val) => { showEditDialog = val; if (!val) editProductErrors.value = {}; }"
    />

    <!-- Delete Product Dialog -->
    <ProductDelete
      v-model:show="showDeleteDialog"
      :loading="deletingProduct"
      :product-data="currentProduct"
      title="Eliminar Producto"
      @confirmDelete="handlerDeleteProduct"
    />
      
</div>
</template>

<style scoped>
.products-page {
  padding: 20px 0;
}
</style>