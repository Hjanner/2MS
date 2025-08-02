<script setup>
import { ref, onMounted } from 'vue';
import ClientList from '@/components/client/ClientList.vue';
import ClientForm from '@/components/client/ClientForm.vue';
import ClientDelete from '@/components/client/ClientDelete.vue';
import BacktoHome from '@/components/BacktoHome.vue';
import api from '@/api/api';

const clientes = ref([]);
const loading = ref(false);
const addingClient = ref(false);
const editingClient = ref(false);
const deletingClient = ref(false);
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDeleteDialog = ref(false);
const currentClient = ref(null);

async function fetchClientes() {
  loading.value = true;
  try {
    const response = await api.get('/clientes');
    clientes.value = response.data;
  } catch (error) {
    console.error('Error fetching clients:', error);
  } finally {
    loading.value = false;
  }
}

async function handleAddClient(clientData) {
  addingClient.value = true;
  try {
    await api.post('/clientes', clientData);
    await fetchClientes();
    showAddDialog.value = false;
  } catch (error) {
    console.error('Error adding client:', error);
  } finally {
    addingClient.value = false;
  } 
}

async function handlerEditClient(clientData) {
  editingClient.value = true;
  try {
    await api.put(`/clientes/${currentClient.value.ci_cliente}`, clientData);
    await fetchClientes();
    showEditDialog.value = false;
    currentClient.value = null;
  } catch (error) {
    console.error('Error editing client:', error);
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
  } catch (error) {
    console.error('Error deleting client:', error);
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
              <client-list 
                :clientes="clientes" 
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
      @submit="handleAddClient"
    />

    <!-- Edit Client Dialog -->
    <ClientForm
      v-model:show="showEditDialog"
      :loading="editingClient"
      :client-data="currentClient"
      title="Editar Cliente"
      @submit="handlerEditClient"
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
