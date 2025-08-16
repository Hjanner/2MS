<script>
import ReloadButton from '@/components/common/ReloadButton.vue';

export default {
  name: 'SupplierList',
  props: {
    proveedores: {
      type: Array,
      required: true,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      headers: [
        { title: 'RIF', key: 'Rif', sortable: false },
        { title: 'Razón Social', key: 'razon_social' },
        { title: 'Teléfono', key: 'tfl', sortable: false },
        { title: 'Persona Contacto', key: 'persona_contacto' },
        { title: 'Dirección', key: 'direccion', sortable: false },
        { title: 'Acciones', key: 'actions', sortable: false },
      ],
    };
  },
  emits: ['refresh', 'edit', 'delete', 'info']
};
</script>

<template>
  <div class="supplier-list">
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-4"
    ></v-progress-linear>

    <v-alert
      v-if="!loading && proveedores.length === 0"
      type="info"
      class="mb-4"
    >
      No se encontraron proveedores.
    </v-alert>

    <!-- render de lista de datos -->
    <v-data-table 
      :headers="headers"
      :items="proveedores"
      :loading="loading"
      item-key="Rif"
      class="elevation-1"
    >
      <!-- Formatear columna de teléfono -->
      <template v-slot:item.tfl="{ item }">
        {{ item.tfl || 'No especificado' }}
      </template>

      <!-- Formatear columna de persona contacto -->
      <template v-slot:item.persona_contacto="{ item }">
        {{ item.persona_contacto || 'No especificado' }}
      </template>

      <!-- Formatear columna de dirección -->
      <template v-slot:item.direccion="{ item }">
        <span class="text-truncate" style="max-width: 200px; display: block;">
          {{ item.direccion || 'No especificado' }}
        </span>
      </template>

      <!-- mostrar botones de accion -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex align-center gap-2 btn-action">
          <v-btn icon size="small" @click="$emit('edit', item)">
            <v-icon>mdi-pencil-outline</v-icon>
          </v-btn>
          <v-btn icon size="small" color="primary" @click="$emit('info', item)">
            <v-icon>mdi-eye-outline</v-icon>
          </v-btn>
        </div>
      </template>
    </v-data-table>

    <ReloadButton @click="$emit('refresh')" />
  </div>
</template>

<style scoped>
.supplier-list {
  width: 100%;
}
.btn-action{
  gap: 1rem;
}
</style>