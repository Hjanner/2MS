<script setup>
import { ref, computed } from 'vue';
import ReloadButton from '@/components/common/ReloadButton.vue';
import ProductDetailRow from '@/components/product/ProductDetailRow.vue';
import ProductForm from '@/components/product/ProductForm.vue';
import LowStockAlert from '@/components/inventory/LowStockAlert.vue';
import InventoryMetrics from '@/components/inventory/InventoryMetrics.vue';

const props = defineProps({
  productos: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['refresh']);

const expandedItems = ref([]);

// Computadas para métricas de inventario
const productosConStockBajo = computed(() => {
  return props.productos.filter(p => 
    p.tipo_producto === 'noPreparado' && 
    p.cant_actual <= p.cant_min
  );
});

const valorTotalInventario = computed(() => {
  return props.productos
    .filter(p => p.tipo_producto === 'noPreparado')
    .reduce((total, p) => total + (p.cant_actual * p.costo_compra), 0);
});

// Función para determinar color del stock
function getStockColor(producto) {
  if (producto.tipo_producto === 'preparado') return 'grey';
  if (producto.cant_actual <= 0) return 'red';
  if (producto.cant_actual <= producto.cant_min) return 'orange';
  return 'green';
}

// Función para determinar el estado del stock
function getStockStatus(producto) {
  if (producto.tipo_producto === 'preparado') return 'N/A';
  if (producto.cant_actual <= 0) return 'Sin stock';
  if (producto.cant_actual <= producto.cant_min) return 'Stock bajo';
  return 'Disponible';
}

// Función para formatear moneda
function formatCurrency(amount) {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(amount);
}

// Headers para la tabla
const headers = [
  // { title: 'Imagen', key: 'img', sortable: false, width: '80px' },
  { title: 'Código', key: 'cod_producto', sortable: true },
  { title: 'Nombre', key: 'nombre', sortable: true },
  { title: 'Categoría', key: 'categoria_descr', sortable: true },
  { title: 'Tipo', key: 'tipo_producto', sortable: true},
  { title: 'Precio USD', key: 'precio_usd', sortable: true },
  { title: 'Stock', key: 'cant_actual', sortable: true },
  { title: 'Estado', key: 'status', sortable: false },
  { title: 'Acciones', key: 'actions', sortable: false, width: '120px' }
];
</script>

<template>
  <div class="inventory-list">
    <!-- Métricas del inventario -->
    <InventoryMetrics
      :low-stock-count="productosConStockBajo.length"
      :total-products="productos.length"
      :total-inventory-value="valorTotalInventario"
    />    

    <!-- Alerta de productos con stock bajo -->
    <LowStockAlert :low-stock-products="productosConStockBajo" />


    <!-- Tabla de productos -->
    <v-data-table
      :headers="headers"
      :items="productos"
      :loading="loading"
      loading-text="Cargando inventario..."
      no-data-text="No hay productos en el inventario"
      :items-per-page="10"
      :items-per-page-options="[5, 10, 25, 50, -1]"
      v-model:expanded="expandedItems"
      show-expand
      class="elevation-1"
    >
      <!-- Columna de imagen -->
      <template v-slot:item.img="{ item }">
        <v-avatar size="48" class="ma-1">
          <v-img
            v-if="item.img"
            :src="item.img"
            :alt="item.nombre"
            cover
          />
          <v-icon v-else color="grey-lighten-1">
            mdi-image-off
          </v-icon>
        </v-avatar>
      </template>

      <!-- Columna de tipo de producto -->
      <template v-slot:item.tipo_producto="{ item }">
        <v-chip
          :color="item.tipo_producto === 'preparado' ? 'orange' : 'blue'"
          variant="tonal"
          size="small"
        >
          <v-icon start>
            {{ item.tipo_producto === 'preparado' ? 'mdi-chef-hat' : 'mdi-package-variant' }}
          </v-icon>
          {{ item.tipo_producto === 'preparado' ? 'Preparado' : 'No Preparado' }}
        </v-chip>
      </template>

      <!-- Columna de precio -->
      <template v-slot:item.precio_usd="{ item }">
        <span class="font-weight-medium">
          {{ formatCurrency(item.precio_usd) }}
        </span>
      </template>

      <!-- Columna de stock -->
      <template v-slot:item.cant_actual="{ item }">
        <div v-if="item.tipo_producto === 'noPreparado'">
          <v-chip
            :color="getStockColor(item)"
            variant="tonal"
            size="small"
          >
            {{ item.cant_actual }} {{ item.unidad_medida }}
          </v-chip>
        </div>
        <v-chip v-else color="grey" variant="tonal" size="small">
          N/A
        </v-chip>
      </template>

      <!-- Columna de estado -->
      <template v-slot:item.status="{ item }">
        <v-chip
          :color="getStockColor(item)"
          variant="tonal"
          size="small"
        >
          <v-icon start size="16">
            {{ item.tipo_producto === 'preparado' ? 'mdi-chef-hat' : 
               item.cant_actual <= 0 ? 'mdi-alert-circle' :
               item.cant_actual <= item.cant_min ? 'mdi-alert' : 'mdi-check-circle' }}
          </v-icon>
          {{ getStockStatus(item) }}
        </v-chip>
      </template>

      <!-- Columna de acciones -->
      <template v-slot:item.actions="{ item }">
        <v-btn-group variant="text" density="compact" class="btn-action">
          <v-tooltip text="Ver detalles">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-eye"
                size="small"
                @click="expandedItems = expandedItems.includes(item) ? 
                  expandedItems.filter(i => i !== item) : [...expandedItems, item]"
              />
            </template>
          </v-tooltip>
          
          <v-tooltip v-if="item.tipo_producto === 'noPreparado'" text="Ajustar stock">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-package-variant-plus"
                size="small"
                color="primary"
              />
            </template>
          </v-tooltip>
        </v-btn-group>
      </template>

       <!-- Fila expandida con detalles -->
      <template v-slot:expanded-row="{ item, columns }">
        <td :colspan="columns.length">
          <ProductDetailRow :item="item" />
        </td>
      </template>

      <!-- Template cuando no hay datos -->
      <template v-slot:no-data>
        <div class="text-center pa-4">
          <v-icon size="48" color="grey-lighten-1" class="mb-4">
            mdi-package-variant-off
          </v-icon>
          <div class="text-h6 mb-2">No hay productos en el inventario</div>
          <div class="text-subtitle-1 text-grey">
            Los productos aparecerán aquí cuando sean agregados al sistema.
          </div>
        </div>
      </template>
    </v-data-table>

      <!-- boton de actualizar lista -->
      <ReloadButton :loading="loading" @click="$emit('refresh')" />
  </div>
</template>

<style scoped>
.inventory-list {
  width: 100%;
}

.v-data-table {
  background-color: transparent;
}

.text-h6 {
  font-weight: 600;
}

.font-weight-medium {
  font-weight: 500;
}

.btn-action{
  gap: 1rem;
}
</style>