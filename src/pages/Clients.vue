<script setup>
import { ref, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar.js';
import ClientList from '@/components/client/ClientList.vue';
import ClientForm from '@/components/client/ClientForm.vue';
import ClientDelete from '@/components/client/ClientDelete.vue';
import SearchFilter from '@/components/common/SearchFilter.vue'; 
import BacktoHome from '@/components/common/BacktoHome.vue';
import api from '@/api/api.js';

const clientes = ref([]);
const filteredClientes = ref([]);
const loading = ref(false);
const addingClient = ref(false);
const editingClient = ref(false);
const deletingClient = ref(false);
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDeleteDialog = ref(false);
const currentClient = ref(null);
const { showSnackbar } = useSnackbar();
const addClientErrors = ref({});
const editClientErrors = ref({});

async function fetchClientes() {
  loading.value = true;
  try {
    const response = await api.get('/clientes');
    clientes.value = response.data;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar los clientes';
    showSnackbar(message, 'error');
  } finally { 
    loading.value = false;
  }
}

async function handleAddClient(clientData) {
  addingClient.value = true;
  addClientErrors.value = {};
  
  try {
    await api.post('/clientes', clientData);
    await fetchClientes();
    showAddDialog.value = false;
    showSnackbar('Cliente agregado correctamente', 'success');
  } catch (error) {    
    if (error.response) {
      // console.log('Status:', error.response.status);
      // console.log('Data:', error.response.data);
      const backendErrors = {};

      if (error.response?.data?.detail) {
        const errorDetail = error.response.data.detail;

        if (Array.isArray(errorDetail)) {   // en caso de multiples erroes
          errorDetail.forEach(err => {
            if (err.loc && err.loc.length > 1) {
              backendErrors[err.loc[1]] = err.msg;
              }
          });
        }
        else if (typeof errorDetail === 'object' && errorDetail.field) {
          backendErrors[errorDetail.field] = errorDetail.message;
        }

        addClientErrors.value = backendErrors;
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
    addingClient.value = false;
  }
}

async function handlerEditClient(clientData) {
  editingClient.value = true;
  editClientErrors.value = {};
  try {
    await api.put(`/clientes/${currentClient.value.ci_cliente}`, clientData);
    await fetchClientes();
    showEditDialog.value = false;
    currentClient.value = null;
    showSnackbar('Cliente editado correctamente', 'success');
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
      editClientErrors.value = backendErrors;
    } else {
      const message = error.response?.data?.message || 'Error al editar el cliente';
      showSnackbar(message, 'error');
    }
  } finally {
    editingClient.value = false;
  }
}

async function handlerDeleteClient(ci_cliente) {
  deletingClient.value = true;
  try {
    await api.delete(`/clientes/${ci_cliente}`);
    await fetchClientes();
    showDeleteDialog.value = false;
    currentClient.value = null;
    showSnackbar('Cliente eliminado correctamente', 'success');
  } catch (error) {
    const message = error.response?.data?.message || 'Error al eliminar el cliente';
    showSnackbar(message, 'error');
  } finally {
    deletingClient.value = false;
  }
}

function handleEditClick(cliente) {
  currentClient.value = cliente;
  showEditDialog.value = true;
}

function handleDeleteClick(cliente) {    
  currentClient.value = cliente;  
  showDeleteDialog.value = true;
}


// Manejar los datos filtrados del componente de búsqueda
function handleFilteredData(filtered) {
  filteredClientes.value = filtered;
}

// Opcional: manejar eventos de búsqueda para analytics o logs
// function handleSearch(searchData) {
//   console.log('Búsqueda realizada:', searchData);
// }

onMounted(() => {
  fetchClientes();
});
</script>

<template>
  <div class="clients-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <backto-home></backto-home>
          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Gestión de Clientes</span>
              <v-btn
                color="primary"
                @click="showAddDialog = true"
              >
                <v-icon left>mdi-plus</v-icon>
                Agregar Cliente
              </v-btn>
            </v-card-title>
            
            <v-card-text>
                <!-- Componente de búsqueda -->
                <SearchFilter
                  :data="clientes"
                  :search-fields="['ci_cliente', 'nombre', 'tlf', 'depto_escuela']"
                  placeholder="Buscar clientes por nombre, CI, teléfono o departamento..."
                  :show-field-filter="true"
                  result-text="clientes"
                  @filtered="handleFilteredData"
                  @search="handleSearch"
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

    <!-- Add Client Dialog -->
    <ClientForm
      v-model:show="showAddDialog"
      :loading="addingClient"
      title="Agregar Nuevo Cliente"
      :errors="addClientErrors"
      @submit="handleAddClient"
      @update:show="(val) => { showAddDialog = val; if (!val) addClientErrors.value = {}; }"
    />

    <!-- Edit Client Dialog -->
    <ClientForm
      v-model:show="showEditDialog"
      :loading="editingClient"
      :client-data="currentClient"
      title="Editar Cliente"
      :errors="editClientErrors"
      @submit="handlerEditClient"
      @update:show="(val) => { showEditDialog = val; if (!val) editClientErrors.value = {}; }"
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
