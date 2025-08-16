<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  lowStockProducts: {
    type: Array,
    default: () => []
  },
  outOfStockProducts: {
    type: Array,
    default: () => []
  }
});

const totalCriticalProducts = computed(() => {
  return props.lowStockProducts.length + props.outOfStockProducts.length
});

const alertType = computed(() => {
  if (props.outOfStockProducts.length > 0) return 'error'
  if (props.lowStockProducts.length > 0) return 'warning'
  return 'info'
});

const alertTitle = computed(() => {
  if (props.outOfStockProducts.length > 0) {
    return 'Productos sin stock'
  }
  return 'Productos con stock bajo'
});
</script>

<template>
  <v-alert
    v-if="totalCriticalProducts > 0"
    :type="alertType"
    variant="tonal"
    closable
    class="ma-3"
  >
    <v-alert-title>
      <!-- <v-icon>{{ alertType === 'error' ? 'mdi-alert-circle' : 'mdi-alert' }}</v-icon> -->
      {{ alertTitle }}
    </v-alert-title>
    
    <div class="mt-2">
      <!-- Productos sin stock -->
      <div v-if="outOfStockProducts.length > 0" class="mb-2">
        <div class="text-subtitle-2 text-error mb-1">Sin stock ({{ outOfStockProducts.length }}):</div>
        <v-chip
          v-for="producto in outOfStockProducts.slice(0, 3)"
          :key="producto.cod_producto_noPreparado"
          size="small"
          color="error"
          variant="outlined"
          class="me-1 mt-1"
        >
          {{ producto.nombre || producto.cod_producto_noPreparado }} (0)
        </v-chip>
        <span v-if="outOfStockProducts.length > 3" class="text-caption">
          y {{ outOfStockProducts.length - 3 }} más...
        </span>
      </div>
      
      <!-- Productos con stock bajo -->
      <div v-if="lowStockProducts.length > 0">
        <div class="text-subtitle-2 text-warning mb-1">Stock bajo ({{ lowStockProducts.length }}):</div>
        <v-chip
          v-for="producto in lowStockProducts.slice(0, 3)"
          :key="producto.cod_producto_noPreparado"
          size="small"
          color="warning"
          variant="outlined"
          class="me-1 mt-1"
        >
          {{ producto.nombre || producto.cod_producto_noPreparado }} ({{ producto.cant_actual }}/{{ producto.cant_min }})
        </v-chip>
        <span v-if="lowStockProducts.length > 3" class="text-caption">
          y {{ lowStockProducts.length - 3 }} más...
        </span>
      </div>
    </div>
  </v-alert>
</template>