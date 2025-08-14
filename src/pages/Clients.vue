<script setup>
import { ref, onMounted } from 'vue';
import { useApiErrorHandler } from '@/composables/useApiErrorHandler';
import { useSnackbar } from '@/composables/useSnackbar';
import ClientList from '@/components/client/ClientList.vue';
import ClientForm from '@/components/client/ClientForm.vue';
import ClientDelete from '@/components/client/ClientDelete.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import api from '@/api/api.js';

const clientes = ref([]);
const filteredClientes = ref([]);
const loading = ref(false);
const deletingClient = ref(false);
const showDeleteDialog = ref(false);
const showClientForm = ref(false);
const formLoading = ref(false);
const formErrors = ref({});
const currentClient = ref(null);

const { handleApiError, handleSuccess } = useApiErrorHandler();
const { showSnackbar } = useSnackbar();

async function fetchClientes() {
  loading.value = true;
  try {
    const response = await api.get('/clientes');
    clientes.value = response.data;
  } catch (error) {
    const errors = handleApiError(error, formErrors);
    if (errors.ci_cliente) {
      // Resaltar campo de cédula en tu UI
    }
  } finally { 
    loading.value = false;
  }
}

async function handleSubmit(clientData) {
  formLoading.value = true;
  formErrors.value = {}; // Limpiar errores antes de enviar
  
  try {
    if (currentClient.value) {
      await api.put(`/clientes/${currentClient.value.ci_cliente}`, clientData);
      handleSuccess('Cliente actualizado correctamente');
    } else {
      await api.post('/clientes', clientData);
      handleSuccess('Cliente creado correctamente');
    }
    
    showClientForm.value = false;
    await fetchClientes();
  } catch (error) {
    formErrors.value = handleApiError(error);
  } finally {
    formLoading.value = false;
  }
}

function handleAddClient() {
  currentClient.value = null;
  formErrors.value = {}; // Limpiar errores al abrir formulario
  showClientForm.value = true;
}


async function handlerDeleteClient(ci_cliente) {
  deletingClient.value = true;
  try {
    await api.delete(`/clientes/${ci_cliente}`);
    await fetchClientes();
    showDeleteDialog.value = false;
    currentClient.value = null;
    handleSuccess('Cliente eliminado correctamente');
  } catch (error) {
    handleApiError(error);
  } finally {
    deletingClient.value = false;
  }
}

function handleEditClick(client) {
  currentClient.value = client;
  showClientForm.value = true;
}

function handleDeleteClick(cliente) {
  currentClient.value = cliente;
  showDeleteDialog.value = true;
}

function handleFilteredData(filtered) {
  filteredClientes.value = filtered;
}

onMounted(() => {
  fetchClientes();
});
</script>

<template>
  <div class="clients-page">
    <v-container>
      <v-row>
        <v-col cols="12">          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Gestión de Clientes</span>
              <v-btn 
                color="primary"
                @click="handleAddClient"
              >
                <v-icon left>mdi-plus</v-icon>
                Agregar Cliente
              </v-btn>
            </v-card-title>
            
            <v-card-text>
                <SearchFilter
                  :data="clientes"
                  :search-fields="['ci_cliente', 'nombre', 'tlf', 'depto_escuela']"
                  placeholder="Buscar clientes por nombre, CI, teléfono o departamento..."
                  :show-field-filter="true"
                  result-text="clientes"
                  @filtered="handleFilteredData"
                />

                <client-list 
                  :clientes="filteredClientes" 
                  :loading="loading"
                  @refresh="fetchClientes"
                  @edit="handleEditClick"
                  @delete="handleDeleteClick"
                />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <ClientForm
      v-model:show="showClientForm"
      :title="currentClient ? 'Editar Cliente' : 'Agregar Cliente'"
      :loading="formLoading"
      :client-data="currentClient"
      :errors="formErrors"
      :mode="currentClient ? 'edit' : 'add'"
      @submit="handleSubmit"
    />

  <!-- Delete Client Dialog -->
  <ClientDelete
    v-model:show="showDeleteDialog"
    :loading="deletingClient"
    :client-data="currentClient"
    title="Eliminar Cliente"
    @confirmDelete="handlerDeleteClient"
  />
  </div>
</template>

<style scoped>
.clients-page {
  padding: 20px 0;
}
</style>