<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import ProductList from '@/components/product/ProductList.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/common/BacktoHome.vue';
import api from '@/api/api';

const productos = ref([]);
const filteredProductos = ref([]);
const loading = ref(false);
const addingProduct = ref(false);
const editingProduct = ref(false);
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const currentProduct = ref(null);
const { showSnackbar } = useSnackbar();
const addProductErrors = ref({});
const editProductErrors = ref({});
const categorias = ref([]);

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
    const response = await api.get('/productos');
    // Mapear productos y añadir nombre de categoría    
    productos.value = response.data.map(producto => {
      const categoria = categorias.value.find(c => c.id_categoria === producto.id_categoria);
      return {
        ...producto,
        nombre_categoria: categoria ? categoria.descr : 'Sin categoría'
      };
    });    
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
    
    if (Array.isArray(error.response.data.detail)) {
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

function handleEditClick(producto) {
  currentProduct.value = producto;
  showEditDialog.value = true;
}

// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredProductos.value = filtered;
}

onMounted(async () => {
  await fetchCategorias();
  await fetchProducts();
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
                  :search-fields="['nombre', 'precio', 'nombre_categoria']"
                  placeholder="Buscar productos por nombre, precio o categoría..."
                  :show-field-filter="true"
                  result-text="productos"
                  @filtered="handleFilteredData"
                  @search="handleSearch"
                />

                <product-list 
                  :productos="filteredProductos" 
                  :loading="loading"
                  :categorias="categorias"                  
                  @refresh="fetchProducts"
                  @edit="handleEditClick"
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
      :categorias="categorias"
      :errors="addProductErrors"
      @submit="handleAddProduct"
      @update:show="(val) => { showAddDialog = val; if (!val) addProductErrors.value = {}; }"
    />

    <!-- Edit Product Dialog -->
    <ProductForm
      v-model:show="showEditDialog"
      :loading="editingProduct"
      :product-data="currentProduct"
      :categorias="categorias"
      title="Editar Producto"
      :errors="editProductErrors"
      @submit="handlerEditProduct"
      @update:show="(val) => { showEditDialog = val; if (!val) editProductErrors.value = {}; }"
    />      
</div>
</template>

<style scoped>
.products-page {
  padding: 20px 0;
}
</style>