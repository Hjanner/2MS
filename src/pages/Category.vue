<script setup>
import { ref, onMounted } from 'vue';
import { useApiErrorHandler } from '@/composables/useApiErrorHandler';
import { useSnackbar } from '@/composables/useSnackbar';
import CategoryProductList from '@/components/category/CategoryProductList.vue';
import CategoryProductForm from '@/components/category/CategoryProductForm.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import api from '@/api/api.js';

const categorias = ref([]);
const filteredCategorias = ref([]);
const loading = ref(false);
const deletingCategory = ref(false);
const showDeleteDialog = ref(false);
const showCategoryForm = ref(false);
const formLoading = ref(false);
const formErrors = ref({});
const currentCategory = ref(null);

const { handleApiError, handleSuccess } = useApiErrorHandler();
const { showSnackbar } = useSnackbar();

async function fetchCategorias() {
  loading.value = true;
  try {
    const response = await api.get('/categoria_productos');
    categorias.value = response.data;
  } catch (error) {
    handleApiError(error);
  } finally { 
    loading.value = false;
  }
}

async function handleSubmit(categoryData) {
  formLoading.value = true;
  formErrors.value = {};
  
  try {
    if (currentCategory.value) {
      await api.put(`/categoria_productos/${currentCategory.value.id_categoria}`, categoryData);
      handleSuccess('Categoría actualizada correctamente');
    } else {
      await api.post('/categoria_productos', categoryData);
      handleSuccess('Categoría creada correctamente');
    }
    
    showCategoryForm.value = false;
    await fetchCategorias();
  } catch (error) {
    handleApiError(error, formErrors);
  } finally {
    formLoading.value = false;
  }
}

async function handlerDeleteCategory(id_categoria) {
  deletingCategory.value = true;
  try {
    await api.delete(`/categoria_productos/${id_categoria}`);
    await fetchCategorias();
    showDeleteDialog.value = false;
    currentCategory.value = null;
    handleSuccess('Categoría eliminada correctamente');
  } catch (error) {
    handleApiError(error);
  } finally {
    deletingCategory.value = false;
  }
}

function handleAddCategory() {
  currentCategory.value = null;
  showCategoryForm.value = true;
}

function handleEditClick(category) {
  currentCategory.value = category;
  showCategoryForm.value = true;
}

function handleDeleteClick(category) {
  currentCategory.value = category;
  showDeleteDialog.value = true;
}

function handleFilteredData(filtered) {
  filteredCategorias.value = filtered;
}

onMounted(() => {
  fetchCategorias();
});
</script>

<template>
  <div class="categories-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Gestión de Categorías de Productos</span>
              <v-btn 
                color="primary"
                @click="handleAddCategory"
              >
                <v-icon left>mdi-plus</v-icon>
                Agregar Categoría
              </v-btn>
            </v-card-title>
            
            <v-card-text>
                <SearchFilter
                  :data="categorias"
                  :search-fields="['descr', 'tipo']"
                  placeholder="Buscar categorías por descripción o tipo..."
                  :show-field-filter="true"
                  result-text="categorías"
                  @filtered="handleFilteredData"
                />

                <category-product-list 
                  :categorias="filteredCategorias" 
                  :loading="loading"
                  @refresh="fetchCategorias"
                  @edit="handleEditClick"
                  @delete="handleDeleteClick"
                />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <CategoryProductForm
      v-model:show="showCategoryForm"
      :title="currentCategory ? 'Editar Categoría' : 'Agregar Categoría'"
      :loading="formLoading"
      :category-data="currentCategory"
      :errors="formErrors"
      :mode="currentCategory ? 'edit' : 'add'"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped>
.categories-page {
  padding: 20px 0;
}
</style>