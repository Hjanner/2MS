<script setup>
import { ref, computed } from 'vue';
import api from '@/api/api';
import { useSnackbar } from '@/composables/useSnackbar';
import { formatCurrencyBs } from '@/utils/formatters';

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
const showDeleteDialog = ref(false);
const compraToDelete = ref(null);
const deleting = ref(false);
const showDetailsDialog = ref(false);
const currentCompraDetails = ref(null);
const loadingDetails = ref(false);

// Headers para la tabla
const headers = [
//   { title: 'ID', value: 'id_compra', sortable: true },
  { title: 'Fecha', value: 'fecha_formatted', sortable: true },
  { title: 'Proveedor', value: 'proveedor_nombre', sortable: true },
  { title: 'Gasto Total (BS)', value: 'gasto_total', sortable: true },
  { title: 'Acciones', value: 'actions', sortable: false, align: 'center' }
];

// Obtener detalles de una compra específica
async function getCompraDetails(idCompra) {
  loadingDetails.value = true;
  try {
    const response = await api.get(`/compras/${idCompra}`);
    currentCompraDetails.value = response.data;
    showDetailsDialog.value = true;
  } catch (error) {
    showSnackbar('Error al cargar detalles de la compra', 'error');
  } finally {
    loadingDetails.value = false;
  }
}

// Emitir evento de edición
function editCompra(compra) {
  emit('edit', compra);
}

// Cerrar diálogo de detalles
function closeDetailsDialog() {
  showDetailsDialog.value = false;
  currentCompraDetails.value = null;
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
          <v-icon size="small" class="mr-2" color="primary">
            mdi-truck-delivery
          </v-icon>
          {{ item.proveedor_nombre }}
        </div>
      </template>

      <!-- Slot para acciones -->
      <template #item.actions="{ item }">
        <div class="d-flex justify-center">
          <v-tooltip text="Ver detalles">
            <template #activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-eye"
                size="small"
                variant="text"
                color="info"
                @click="getCompraDetails(item.id_compra)"
                :loading="loadingDetails && currentCompraDetails?.id_compra === item.id_compra"
              />
            </template>
          </v-tooltip>
        </div>
      </template>

      <!-- Slot para estado vacío -->
      <template #no-data>
        <div class="text-center pa-4">
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
    </v-data-table>

    <!-- Dialog de confirmación para eliminar -->
    <v-dialog
      v-model="showDeleteDialog"
      max-width="400"
      persistent
    >
      <v-card>
        <v-card-title class="text-h6">
          Confirmar Eliminación
        </v-card-title>
        
        <v-card-text>
          ¿Estás seguro de que deseas eliminar la compra #{{ compraToDelete?.id_compra }}?
          <br>
          <strong>Esta acción no se puede deshacer.</strong>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn
            text
            @click="showDeleteDialog = false"
            :disabled="deleting"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            @click="deleteCompra"
            :loading="deleting"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de detalles de la compra -->
    <v-dialog
      v-model="showDetailsDialog"
      max-width="800"
      scrollable
    >
      <v-card v-if="currentCompraDetails">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-receipt</v-icon>
          Detalles de Compra #{{ currentCompraDetails.id_compra }}
          <v-spacer />
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="closeDetailsDialog"
          />
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-6">
          <!-- Información general -->
          <div class="mb-6">
            <h3 class="text-h6 mb-3">Información General</h3>
            <v-row>
              <v-col cols="12" md="6">
                <div class="text-subtitle-2 text-grey-darken-1">Fecha</div>
                <div class="text-body-1">{{ new Date(currentCompraDetails.fecha).toLocaleDateString('es-ES') }}</div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="text-subtitle-2 text-grey-darken-1">Proveedor</div>
                <div class="text-body-1">{{ currentCompraDetails.proveedor?.razon_social || 'Sin proveedor' }}</div>
              </v-col>
              <v-col cols="12">
                <div class="text-subtitle-2 text-grey-darken-1">Gasto Total</div>
                <div class="text-h6 text-success">{{ formatCurrencyBs(currentCompraDetails.gasto_total) }}</div>
              </v-col>
            </v-row>
          </div>

          <!-- Productos comprados -->
          <div v-if="currentCompraDetails.productos && currentCompraDetails.productos.length">
            <h3 class="text-h6 mb-3">Productos Comprados</h3>
            <v-data-table
              :headers="[
                { title: 'Producto', value: 'nombre' },
                { title: 'Cantidad', value: 'cantidad' },
                { title: 'Costo Unitario', value: 'costo_unitario' },
                { title: 'Subtotal', value: 'subtotal' }
              ]"
              :items="currentCompraDetails.productos.map(p => ({
                ...p,
                subtotal: p.cantidad * p.costo_unitario
              }))"
              hide-default-footer
              class="elevation-1"
            >
              <template #item.costo_unitario="{ item }">
                {{ formatCurrencyBs(item.costo_unitario) }}
              </template>
              <template #item.subtotal="{ item }">
                <span class="font-weight-medium">
                  {{ formatCurrencyBs(item.subtotal) }}
                </span>
              </template>
            </v-data-table>
          </div>
        </v-card-text>

        <v-divider />

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            @click="closeDetailsDialog"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.compras-list {
  margin-top: 20px;
}
</style>
<!-- 
<v-tooltip text="Editar">
    <template #activator="{ props }">
        <v-btn
        v-bind="props"
        icon="mdi-pencil"
        size="small"
        variant="text"
        color="warning"
        @click="editCompra(item)"
        />
    </template>
</v-tooltip> -->