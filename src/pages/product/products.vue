<script setup>
import { ref, onMounted } from 'vue';
import ProductList from '@/components/product/ProductList.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import ProductDelete from '@/components/product/ProductDelete.vue';
import BacktoHome from '@/components/BacktoHome.vue';
import api from '@/api/api';

const productos = ref([]);
const loading = ref(false);
const addingProduct = ref(false);
const editingProduct = ref(false);
const deletingProduct = ref(false);
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDeleteDialog = ref(false);
const currentProduct = ref(null);

async function fetchProducts() {
  loading.value = true;
  try {
    const response = await api.get('/productos');
    productos.value = response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
  } finally {
    loading.value = false;
  }
}

async function handleAddProduct(productData) {
  addingProduct.value = true;
  try {
    await api.post('/productos', productData);
    await fetchProducts();
    showAddDialog.value = false;
  } catch (error) {
    console.error('Error adding product:', error);
  } finally {
    addingProduct.value = false;
  } 
}

async function handlerEditProduct(productData) {
  editingProduct.value = true;
  try {
    await api.put(`/productos/${currentProduct.value.ci_producto}`, productData);
    await fetchProducts();
    showEditDialog.value = false;
    currentProduct.value = null;
  } catch (error) {
    console.error('Error editing product:', error);
  } finally {
    editingProduct.value = false;
  }
}

async function handlerDeleteProduct(ci_producto) {
  deletingProduct.value = true;
  try {
    await api.delete(`/productos/${ci_producto}`);
    await fetchProducts();
    showDeleteDialog.value = false;
    currentProduct.value = null;
  } catch (error) {
    console.error('Error deleting product:', error);
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
              <product-list 
                :productos="productos" 
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

    <ProductForm
      v-model:show="showAddDialog"
      :loading="addingProduct" 
      title="Agregar Nuevo Producto"
      @submit="handleAddProduct"
    />

    <ProductForm
      v-model:show="showEditDialog"
      :loading="editingProduct"
      :product-data="currentProduct"
      title="Editar Producto"
      @submit="handlerEditProduct"
    />

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