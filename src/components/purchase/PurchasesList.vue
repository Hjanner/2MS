<script setup>
import { ref } from 'vue';
import api from '@/api/api';
import { useSnackbar } from '@/composables/useSnackbar';
import { formatCurrencyBs } from '@/utils/formatters';
import PurchaseDetailDialog from '@/components/purchase/PurchaseDetailDialog.vue';

const props = defineProps({
  compras: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  proveedores: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['refresh', 'edit']);
const { showSnackbar } = useSnackbar();


// Estado para controlar el diálogo de detalles
const detailDialog = ref({
  show: false,
  purchaseDetails: null,
  loading: false
});

// Headers para la tabla
const headers = [
  { title: 'ID Compra', value: 'id_compra', sortable: true },
  { title: 'Fecha', value: 'fecha_formatted', sortable: true },
  { title: 'Proveedor', value: 'proveedor_nombre', sortable: true },
  { title: 'Gasto Total (BS)', value: 'gasto_total', sortable: true },
  { title: 'Acciones', value: 'actions', sortable: false, align: 'center' }
];

// Obtener detalles de una compra específica usando el endpoint correcto
async function getCompraDetails(idCompra) {
  detailDialog.value = {
    show: true,
    purchaseDetails: null,
    loading: true
  };
  
  try {
    const response = await api.get(`/vista/${idCompra}/detalle`);
    detailDialog.value.purchaseDetails = response.data;
  } catch (error) {
    const message = error.response?.data?.message || 'Error al cargar detalles de la compra';
    showSnackbar(message, 'error');
    detailDialog.value.show = false;
  } finally {
    detailDialog.value.loading = false;
  }
}

// Función para obtener el nombre del proveedor
function getProveedorNombre(rif) {
  const proveedor = props.proveedores.find(p => p.Rif === rif);
  return proveedor ? proveedor.razon_social : rif || 'Sin proveedor';
}

// Cerrar el diálogo de detalles
function closeDetailDialog() {
  detailDialog.value = {
    show: false,
    purchaseDetails: null,
    loading: false
  };
}
</script>

<template>
  <div class="compras-list">
    <v-data-table
      :headers="headers"
      :items="compras"
      :loading="loading"
      loading-text="Cargando compras..."
      no-data-text="No hay compras registradas"
      items-per-page-text="Compras por página:"
      :items-per-page-options="[
        { value: 10, title: '10' },
        { value: 25, title: '25' },
        { value: 50, title: '50' },
        { value: -1, title: 'Todas' }
      ]"
      class="elevation-1"
    >
      <!-- Slot para ID de compra -->
      <template #item.id_compra="{ item }">
          {{ item.id_compra }}
      </template>

      <!-- Slot para gasto total -->
      <template #item.gasto_total="{ item }">
        <span class="font-weight-medium text-success">
          {{ formatCurrencyBs(item.gasto_total) }}
        </span>
      </template>

      <!-- Slot para fecha -->
      <template #item.fecha_formatted="{ item }">
        <v-chip
          size="small"
          color="blue-grey"
          variant="tonal"
        >
          {{ item.fecha_formatted }}
        </v-chip>
      </template>

      <!-- Slot para proveedor -->
      <template #item.proveedor_nombre="{ item }">
        <div class="d-flex align-center">
          <v-icon 
            left 
            size="small" 
            color="grey-darken-1" 
            class="mr-2"
          >
            mdi-truck
          </v-icon>
          {{ getProveedorNombre(item.Rif) }}
        </div>
      </template>

      <!-- Slot para acciones -->
      <template #item.actions="{ item }">
          <v-tooltip text="Ver detalles">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-eye-outline"
                size="small"
                color="primary"
                @click="getCompraDetails(item.id_compra)"
                :loading="detailDialog.loading && detailDialog.purchaseDetails?.compra?.id_compra === item.id_compra"
              />
            </template>
          </v-tooltip>
      </template>

      <!-- Slot para estado vacío -->
      <template #no-data>
        <div class="text-center pa-8">
          <v-icon size="64" color="grey-lighten-2">
            mdi-cart-off
          </v-icon>
          <div class="text-h6 text-grey-lighten-1 mt-2">
            No hay compras registradas
          </div>
          <div class="text-body-2 text-grey-lighten-1">
            Las compras aparecerán aquí una vez que registres la primera
          </div>
        </div>
      </template>

      <!-- Slot para loading -->
      <template #loading>
        <div class="text-center pa-4">
          <v-progress-circular
            indeterminate
            color="primary"
            size="48"
          />
          <div class="mt-2 text-body-2 text-grey-darken-1">
            Cargando compras...
          </div>
        </div>
      </template>
    </v-data-table>
    
    <!-- Diálogo de detalles de compra -->
    <PurchaseDetailDialog
      :show="detailDialog.show"
      :purchase-details="detailDialog.purchaseDetails"
      :loading="detailDialog.loading"
      @update:show="closeDetailDialog"
    />
  </div>
</template>

<style scoped>
.compras-list {
  margin-top: 20px;
}

.v-data-table {
  border-radius: 8px;
}

.d-flex.gap-1 {
  gap: 4px;
}
</style>