<!-- InventoryMetrics.vue (Componente reutilizable) -->
<script setup>
import { defineProps, computed } from 'vue';
import { formatCurrency } from '@/utils/formatters';

const props = defineProps({
  lowStockCount: Number,
  totalProducts: Number,
  totalInventoryValue: Number
});

const formattedTotalValue = computed(() => formatCurrency(props.totalInventoryValue));
</script>

<template>
  <v-row class="mb-4">
    <v-col cols="12" md="4">
      <v-card color="error" variant="tonal" class="pa-4">
        <div class="d-flex align-center">
          <v-icon size="40" color="error" class="me-3">mdi-alert</v-icon>
          <div>
            <div class="text-h6">{{ lowStockCount }}</div>
            <div class="text-subtitle-2">Productos con stock bajo</div>
          </div>
        </div>
      </v-card>
    </v-col>
    
    <v-col cols="12" md="4">
      <v-card color="primary" variant="tonal" class="pa-4">
        <div class="d-flex align-center">
          <v-icon size="40" color="primary" class="me-3">mdi-package-variant-closed</v-icon>
          <div>
            <div class="text-h6">{{ totalProducts }}</div>
            <div class="text-subtitle-2">Total productos</div>
          </div>
        </div>
      </v-card>
    </v-col>
    
    <v-col cols="12" md="4">
      <v-card color="success" variant="tonal" class="pa-4">
        <div class="d-flex align-center">
          <v-icon size="40" color="success" class="me-3">mdi-cash</v-icon>
          <div>
            <div class="text-h6">{{ formattedTotalValue }}</div>
            <div class="text-subtitle-2">Valor total inventario</div>
          </div>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>