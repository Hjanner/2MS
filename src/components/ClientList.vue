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
      No clients found.
    </v-alert>

    <v-list v-else>
      <v-list-item
        v-for="cliente in clientes"
        :key="cliente.id"
        class="mb-2"
      >
        <v-list-item-content>
          <v-list-item-title>{{ cliente.ci_cliente }}</v-list-item-title>
          <v-list-item-title>{{ cliente.nombre }}</v-list-item-title>
        </v-list-item-content>
        
        <v-list-item-action>
          <v-btn
            icon
            @click="$emit('edit', cliente)"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-item-action>
        
        <v-list-item-action>
          <v-btn
            icon
            color="error"
            @click="$emit('delete', cliente.id)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>

    <div class="d-flex justify-end mt-4">
      <v-btn
        color="primary"
        @click="$emit('refresh')"
        :loading="loading"
      >
        <v-icon left>mdi-refresh</v-icon>
        Refresh List
      </v-btn>
    </div>
  </div>
</template>

<script>
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
    }
  },
  emits: ['refresh', 'edit', 'delete']
};
</script>

<style scoped>
.client-list {
  width: 100%;
}
</style>
