<script>
import ReloadButton from '@/components/common/ReloadButton.vue';

export default {
  name: 'CategoryProductList',
  props: {
    categorias: {
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
        { title: 'ID', key: 'id_categoria', sortable: true, width: '100px' },
        { title: 'Descripción', key: 'descr', sortable: true },
        { title: 'Tipo', key: 'tipo', sortable: true, width: '150px' },
        { title: 'Acciones', key: 'actions', sortable: false, width: '200px' },
      ],
      typeColors: {
        'preparado': 'success',
        'noPreparado': 'warning'
      },
      typeLabels: {
        'preparado': 'Preparado',
        'noPreparado': 'No Preparado'
      }
    };
  },
  emits: ['refresh', 'edit', 'delete', 'info']
};
</script>

<template>
  <div class="category-list">
    <v-progress-linear
      v-if="loading"
      indeterminate
      color="primary"
      class="mb-4"
    ></v-progress-linear>

    <v-alert
      v-if="!loading && categorias.length === 0"
      type="info"
      class="mb-4"
    >
      No se encontraron categorías.
    </v-alert>

    <!-- render de lista de datos -->
    <v-data-table 
      :headers="headers"
      :items="categorias"
      :loading="loading"
      item-key="id_categoria"
      class="elevation-1"
    >
      <!-- Formatear columna de ID -->
      <template v-slot:item.id_categoria="{ item }">
        <v-chip
          size="small"
          color="primary"
          variant="outlined"
        >
          #{{ item.id_categoria }}
        </v-chip>
      </template>

      <!-- Formatear columna de tipo con chips de colores -->
      <template v-slot:item.tipo="{ item }">
        <v-chip
          :color="typeColors[item.tipo] || 'default'"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ item.tipo === 'preparado' ? 'mdi-chef-hat' : 'mdi-package-variant' }}
          </v-icon>
          {{ typeLabels[item.tipo] || item.tipo }}
        </v-chip>
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
.category-list {
  width: 100%;
}
.btn-action{
  gap: 1rem;
}
</style>