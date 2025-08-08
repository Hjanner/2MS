<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar.js';
import ProductList from '@/components/product/ProductList.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/common/BacktoHome.vue';
import api from '@/api/api.js';

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
    let endpoint = `/productos/${currentProduct.value.cod_producto}`;
    let dataToSend = productData;

    // Determinar endpoint según el tipo de producto
    if (productData.tipo_producto === 'noPreparado') {
      endpoint = `/productos_noPreparados/${currentProduct.value.cod_producto}`;
      dataToSend = {
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
        cant_min: productData.cant_min,
        cant_actual: productData.cant_actual,
        costo_compra: productData.costo_compra,
        unidad_medida: productData.unidad_medida,
        Rif: productData.Rif || null
      };
    } else {
      // Para productos preparados
      dataToSend = {
        nombre: productData.nombre,
        precio_usd: productData.precio_usd,
        img: productData.img,
        id_categoria: productData.id_categoria,
        descr_preparado: productData.descr_preparado || null
      };
    }

    await api.put(endpoint, dataToSend);
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

function handleFilteredData(filtered) {
  filteredProductos.value = filtered;
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
  <div class="products-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <backto-home></backto-home>
          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <div>
                <span class="text-h5">Gestión de Productos</span>
                <div class="text-subtitle-1 mt-2">
                  <v-chip 
                    color="blue" 
                    variant="outlined" 
                    size="small" 
                    class="me-2"
                  >
                    <v-icon start>mdi-package-variant</v-icon>
                    No Preparados: {{ productos.filter(p => p.tipo_producto === 'noPreparado').length }}
                  </v-chip>
                  <v-chip 
                    color="orange" 
                    variant="outlined" 
                    size="small"
                  >
                    <v-icon start>mdi-chef-hat</v-icon>
                    Preparados: {{ productos.filter(p => p.tipo_producto === 'preparado').length }}
                  </v-chip>
                </div>
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
                  :search-fields="['nombre', 'precio_usd', 'nombre_categoria', 'cod_producto', 'tipo_producto']"
                  placeholder="Buscar productos por nombre, precio, categoría, código o tipo..."
                  :show-field-filter="true"
                  result-text="productos"
                  @filtered="handleFilteredData"
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
</div>
</template>

<style scoped>
.products-page {
  padding: 20px 0;
}
</style>