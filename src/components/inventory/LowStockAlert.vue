<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  lowStockProducts: {
    type: Array,
    default: () => []
  }
});
</script>

<template>
  <v-alert
    v-if="lowStockProducts.length > 0"
    type="warning"
    variant="tonal"
    closable
    class="mb-4"
  >
    <v-alert-title>
      <v-icon>mdi-alert</v-icon>
      Productos con stock bajo
    </v-alert-title>
    <div class="mt-2">
      Hay {{ lowStockProducts.length }} productos que necesitan reposición:
      <v-chip
        v-for="producto in lowStockProducts.slice(0, 3)"
        :key="producto.cod_producto"
        size="small"
        color="warning"
        variant="outlined"
        class="me-1 mt-1"
      >
        {{ producto.nombre }} ({{ producto.cant_actual }}/{{ producto.cant_min }})
      </v-chip>
      <span v-if="lowStockProducts.length > 3">
        y {{ lowStockProducts.length - 3 }} más...
      </span>
    </div>
  </v-alert>
</template>