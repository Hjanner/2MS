<template>
  <div class="clients-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-btn
            color="primary"
            class="mb-4"
            @click="$router.push('/')"
          >
            <v-icon left>mdi-arrow-left</v-icon>
            Back to Home
          </v-btn>
          
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Client Management</span>
              <v-btn
                color="primary"
                @click="showAddDialog = true"
              >
                <v-icon left>mdi-plus</v-icon>
                Add Client
              </v-btn>
            </v-card-title>
            
            <v-card-text>
              <client-list 
                :clientes="clientes" 
                :loading="loading"
                @refresh="fetchClientes"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Add Client Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card>
        <v-card-title>Add New Client</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="handleAddClient">
            <v-text-field
              v-model="newClient.nombre"
              label="Name"
              required
              :rules="[v => !!v || 'Name is required']"
              class="mb-4"
            />
            <v-text-field
              v-model="newClient.ci_cliente"
              label="CI"
              required
              :rules="[
                v => !!v || 'CI is required',
                v => /.+@.+\..+/.test(v) || 'Email must be valid',
              ]"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showAddDialog = false">Cancel</v-btn>
          <v-btn 
            color="primary" 
            @click="handleAddClient"
            :loading="addingClient"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ClientList from '@/components/ClientList.vue';
import api from '@/api/api';

const clientes = ref([]);
const loading = ref(false);
const addingClient = ref(false);
const showAddDialog = ref(false);

const newClient = ref({
    ci_cliente: '',
    nombre: '',
    tlf: '',
    depto_escuela: ''
});

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

async function handleAddClient() {
  if (!newClient.value.nombre || !newClient.value.email) return;
  
  addingClient.value = true;
  try {
    await api.post('/clientes', newClient.value);
    await fetchClientes();
    showAddDialog.value = false;
    newClient.value = { nombre: '', email: '' }; // Reset form
  } catch (error) {
    console.error('Error adding client:', error);
  } finally {
    addingClient.value = false;
  }
}

onMounted(() => {
  fetchClientes();
});
</script>

<style scoped>
.clients-page {
  padding: 20px 0;
}
</style>
