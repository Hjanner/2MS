<script setup>
import { ref, onMounted } from 'vue';
import { useApiErrorHandler } from '@/composables/useApiErrorHandler';
import SupplierList from '@/components/supplier/SupplierList.vue';
import SupplierForm from '@/components/supplier/SupplierForm.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import api from '@/api/api.js';

const proveedores = ref([]);
const filteredProveedores = ref([]);
const loading = ref(false);
const showSupplierForm = ref(false);
const formLoading = ref(false);
const formErrors = ref({});
const currentSupplier = ref(null);

const { handleApiError, handleSuccess } = useApiErrorHandler();

async function fetchProveedores() {
  loading.value = true;
  try {
    const response = await api.get('/proveedores');
    proveedores.value = response.data;
  } catch (error) {
    handleApiError(error);
  } finally { 
    loading.value = false;
  }
}

async function handleSubmit(supplierData) {
  formLoading.value = true;
  formErrors.value = {};
  
  try {
    if (currentSupplier.value) {
      await api.put(`/proveedores/${currentSupplier.value.Rif}`, supplierData);
      handleSuccess('Proveedor actualizado correctamente');
    } else {
      await api.post('/proveedores', supplierData);
      handleSuccess('Proveedor creado correctamente');
    }
    
    showSupplierForm.value = false;
    await fetchProveedores();
  } catch (error) {
    handleApiError(error, formErrors);
  } finally {
    formLoading.value = false;
  }
}

function handleAddSupplier() {
  currentSupplier.value = null;
  showSupplierForm.value = true;
}

function handleEditClick(supplier) {
  currentSupplier.value = supplier;
  showSupplierForm.value = true;
}


function handleFilteredData(filtered) {
  filteredProveedores.value = filtered;
}

onMounted(() => {
  fetchProveedores();
});
</script>

<template>
  <div class="suppliers-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Gestión de Proveedores</span>
              <v-btn 
                color="primary"
                @click="handleAddSupplier"
              >
                <v-icon left>mdi-plus</v-icon>
                Agregar Proveedor
              </v-btn>
            </v-card-title>
            
            <v-card-text>
                <SearchFilter
                  :data="proveedores"
                  :search-fields="['Rif', 'razon_social', 'tfl', 'persona_contacto']"
                  placeholder="Buscar proveedores por RIF, razón social, teléfono o contacto..."
                  :show-field-filter="true"
                  result-text="proveedores"
                  @filtered="handleFilteredData"
                />

                <supplier-list 
                  :proveedores="filteredProveedores" 
                  :loading="loading"
                  @refresh="fetchProveedores"
                  @edit="handleEditClick"
                  @delete="handleDeleteClick"
                />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <SupplierForm
      v-model:show="showSupplierForm"
      :title="currentSupplier ? 'Editar Proveedor' : 'Agregar Proveedor'"
      :loading="formLoading"
      :supplier-data="currentSupplier"
      :errors="formErrors"
      :mode="currentSupplier ? 'edit' : 'add'"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped>
.suppliers-page {
  padding: 20px 0;
}
</style>