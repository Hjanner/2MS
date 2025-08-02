<script setup>
import BacktoHome from '@/components/BacktoHome.vue';

</script>

<template>
    <div class="clients-page">
      <v-container>
        <v-row>
          <v-col cols="12">
            <BacktoHome/>
            
            <v-card>
              <v-card-title class="d-flex justify-space-between align-center">
                <span>Product Management</span>
                <v-btn
                  color="primary"
                  @click="showAddDialog = true"
                >
                  <v-icon left>mdi-plus</v-icon>
                  Add Product
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
          <v-card-title>Add New Product</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleAddProduct">
              <v-text-field
                v-model="newProduct.nombre"
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