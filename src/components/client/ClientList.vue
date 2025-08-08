<script>
import ReloadButton from '@/components/common/ReloadButton.vue';

export default {
  name: 'ClientList',
  props: {
    clientes: {
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
        { title: 'C.I. Cliente', key: 'ci_cliente', sortable: false },
        { title: 'Nombre', key: 'nombre' },
        { title: 'Teléfono', key: 'tlf', sortable: false },
        { title: 'Depto/Escuela', key: 'depto_escuela' },
        { title: 'Acciones', key: 'actions', sortable: false },
      ],
    };
  },
  emits: ['refresh', 'edit', 'delete', 'info']
};
</script>

<template>
  <div class="client-list">
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-4"
    ></v-progress-linear>

    <v-alert
      v-if="!loading && clientes.length === 0"
      type="info"
      class="mb-4"
    >
      No se encontraron clientes.
    </v-alert>

    <!-- render de lista de datos -->
    <v-data-table 
      :headers="headers"
      :items="clientes"
      :loading="loading"
      item-key="id"
      class="elevation-1"
    >

      <!-- mostrar botones de accion -->
      <template v-slot:item.actions="{ item }">
        <div class="d-flex align-center gap-2 btn-action">
          <v-btn icon size="small" @click="$emit('edit', item)">
            <v-icon>mdi-pencil-outline</v-icon>
          </v-btn>
          <v-btn icon size="small" color="error" @click="$emit('delete', item)">
            <v-icon>mdi-delete-outline</v-icon>
          </v-btn>
          <v-btn icon size="small" color="primary" @click="$emit('info', item)">
            <v-icon>mdi-information-outline</v-icon>
          </v-btn>
        </div>
      </template>
    </v-data-table>

    <ReloadButton @click="$emit('refresh')" />
  </div>
</template>


<style scoped>
.client-list {
  width: 100%;
}
.btn-action{
  gap: 1rem;
}
</style>
