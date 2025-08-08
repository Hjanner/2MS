<script setup>
import { ref, computed } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import api from '@/api/api';

const props = defineProps({
  productos: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  categorias: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['refresh', 'edit']);

const { showSnackbar } = useSnackbar();
const expandedItems = ref([]);
const deletingProduct = ref(null);
const showDeleteDialog = ref(false);
const productToDelete = ref(null);

// Computadas para métricas
const productosPreparados = computed(() => {
  return props.productos.filter(p => p.tipo_producto === 'preparado');
});

const productosNoPreparados = computed(() => {
  return props.productos.filter(p => p.tipo_producto === 'noPreparado');
});

const productosConStockBajo = computed(() => {
  return productosNoPreparados.value.filter(p => 
    p.cant_actual <= p.cant_min
  );
});

// Headers para la tabla
const headers = [
  { title: 'Imagen', key: 'img', sortable: false, width: '80px' },
  { title: 'Código', key: 'cod_producto', sortable: true },
  { title: 'Nombre', key: 'nombre', sortable: true },
  { title: 'Categoría', key: 'categoria_descr', sortable: true },
  { title: 'Tipo', key: 'tipo_producto', sortable: true },
  { title: 'Precio USD', key: 'precio_usd', sortable: true },
  { title: 'Stock/Estado', key: 'stock', sortable: false },
  { title: 'Acciones', key: 'actions', sortable: false, width: '150px' }
];

// Función para formatear moneda
function formatCurrency(amount) {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(amount);
}

// Función para determinar color del stock
function getStockColor(producto) {
  if (producto.tipo_producto === 'preparado') return 'grey';
  if (producto.cant_actual <= 0) return 'red';
  if (producto.cant_actual <= producto.cant_min) return 'orange';
  return 'green';
}

// Función para obtener el estado del producto
function getProductStatus(producto) {
  if (producto.tipo_producto === 'preparado') {
    return { text: 'Disponible', color: 'green', icon: 'mdi-chef-hat' };
  }
  
  if (producto.cant_actual <= 0) {
    return { text: 'Sin stock', color: 'red', icon: 'mdi-alert-circle' };
  }
  
  if (producto.cant_actual <= producto.cant_min) {
    return { text: 'Stock bajo', color: 'orange', icon: 'mdi-alert' };
  }
  
  return { text: 'Disponible', color: 'green', icon: 'mdi-check-circle' };
}

// Confirmar eliminación
function confirmDelete(producto) {
  productToDelete.value = producto;
  showDeleteDialog.value = true;
}

// Eliminar producto
async function deleteProduct() {
  if (!productToDelete.value) return;
  
  deletingProduct.value = productToDelete.value.cod_producto;
  
  try {
    let endpoint = `/productos/${productToDelete.value.cod_producto}`;
    
    // Usar endpoint específico para productos no preparados
    if (productToDelete.value.tipo_producto === 'noPreparado') {
      endpoint = `/productos_noPreparados/${productToDelete.value.cod_producto}`;
    }
    
    await api.delete(endpoint);
    showSnackbar(`Producto "${productToDelete.value.nombre}" eliminado correctamente`, 'success');
    emit('refresh');
  } catch (error) {
    const message = error.response?.data?.message || 'Error al eliminar el producto';
    showSnackbar(message, 'error');
  } finally {
    deletingProduct.value = null;
    showDeleteDialog.value = false;
    productToDelete.value = null;
  }
}

// Editar producto
function editProduct(producto) {
  emit('edit', producto);
}
</script>

<template>
  <div class="product-list">
    <!-- Métricas de productos -->
    <v-row class="mb-4" v-if="productos.length > 0">
      <v-col cols="12" md="3">
        <v-card color="primary" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-icon size="40" color="primary" class="me-3">mdi-package-variant-closed</v-icon>
            <div>
              <div class="text-h6">{{ productos.length }}</div>
              <div class="text-subtitle-2">Total productos</div>
            </div>
          </div>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card color="blue" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-icon size="40" color="blue" class="me-3">mdi-package-variant</v-icon>
            <div>
              <div class="text-h6">{{ productosNoPreparados.length }}</div>
              <div class="text-subtitle-2">No preparados</div>
            </div>
          </div>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card color="orange" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-icon size="40" color="orange" class="me-3">mdi-chef-hat</v-icon>
            <div>
              <div class="text-h6">{{ productosPreparados.length }}</div>
              <div class="text-subtitle-2">Preparados</div>
            </div>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card color="error" variant="tonal" class="pa-4">
          <div class="d-flex align-center">
            <v-icon size="40" color="error" class="me-3">mdi-alert</v-icon>
            <div>
              <div class="text-h6">{{ productosConStockBajo.length }}</div>
              <div class="text-subtitle-2">Stock bajo</div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Alerta de productos con stock bajo -->
    <v-alert
      v-if="productosConStockBajo.length > 0"
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
        {{ productosConStockBajo.length }} productos necesitan reposición:
        <v-chip
          v-for="producto in productosConStockBajo.slice(0, 3)"
          :key="producto.cod_producto"
          size="small"
          color="warning"
          variant="outlined"
          class="me-1 mt-1"
        >
          {{ producto.nombre }} ({{ producto.cant_actual }}/{{ producto.cant_min }})
        </v-chip>
        <span v-if="productosConStockBajo.length > 3">
          y {{ productosConStockBajo.length - 3 }} más...
        </span>
      </div>
    </v-alert>

    <!-- Tabla de productos -->
    <v-data-table
      :headers="headers"
      :items="productos"
      :loading="loading"
      loading-text="Cargando productos..."
      no-data-text="No hay productos registrados"
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

      <!-- Columna de stock/estado -->
      <template v-slot:item.stock="{ item }">
        <div v-if="item.tipo_producto === 'noPreparado'">
          <v-chip
            :color="getStockColor(item)"
            variant="tonal"
            size="small"
            class="mb-1"
          >
            {{ item.cant_actual }} {{ item.unidad_medida }}
          </v-chip>
          <div class="text-caption">
            Mín: {{ item.cant_min }} {{ item.unidad_medida }}
          </div>
        </div>
        <v-chip 
          v-else 
          :color="getProductStatus(item).color"
          variant="tonal"
          size="small"
        >
          <v-icon start size="16">{{ getProductStatus(item).icon }}</v-icon>
          {{ getProductStatus(item).text }}
        </v-chip>
      </template>

      <!-- Columna de acciones -->
      <template v-slot:item.actions="{ item }">
        <v-btn-group variant="text" density="compact">
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
          
          <v-tooltip text="Editar producto">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-pencil"
                size="small"
                color="primary"
                @click="editProduct(item)"
              />
            </template>
          </v-tooltip>
          
          <v-tooltip text="Eliminar producto">
            <template v-slot:activator="{ props }">
              <v-btn
                v-bind="props"
                icon="mdi-delete"
                size="small"
                color="error"
                :loading="deletingProduct === item.cod_producto"
                @click="confirmDelete(item)"
              />
            </template>
          </v-tooltip>
        </v-btn-group>
      </template>

      <!-- Fila expandida con detalles -->
      <template v-slot:expanded-row="{ item, columns }">
        <td :colspan="columns.length">
          <v-card class="ma-2" variant="tonal">
            <v-card-title class="text-h6 d-flex align-center">
              <v-icon class="me-2">mdi-information</v-icon>
              Detalles de {{ item.nombre }}
            </v-card-title>
            
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <div class="mb-3">
                    <strong>Información básica:</strong>
                  </div>
                  <v-list density="compact">
                    <v-list-item>
                      <v-list-item-title>Código:</v-list-item-title>
                      <v-list-item-subtitle>{{ item.cod_producto }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>Categoría:</v-list-item-title>
                      <v-list-item-subtitle>{{ item.categoria_descr }} ({{ item.categoria_tipo }})</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>Precio de venta:</v-list-item-title>
                      <v-list-item-subtitle>{{ formatCurrency(item.precio_usd) }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>
                
                <v-col cols="12" md="6">
                  <div v-if="item.tipo_producto === 'noPreparado'">
                    <div class="mb-3">
                      <strong>Información de inventario:</strong>
                    </div>
                    <v-list density="compact">
                      <v-list-item>
                        <v-list-item-title>Stock actual:</v-list-item-title>
                        <v-list-item-subtitle>{{ item.cant_actual }} {{ item.unidad_medida }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Stock mínimo:</v-list-item-title>
                        <v-list-item-subtitle>{{ item.cant_min }} {{ item.unidad_medida }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Costo de compra:</v-list-item-title>
                        <v-list-item-subtitle>{{ formatCurrency(item.costo_compra) }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item v-if="item.Rif">
                        <v-list-item-title>Proveedor (RIF):</v-list-item-title>
                        <v-list-item-subtitle>{{ item.Rif }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Margen de ganancia:</v-list-item-title>
                        <v-list-item-subtitle class="font-weight-bold text-success">
                          {{ formatCurrency(item.precio_usd - item.costo_compra) }}
                          ({{ Math.round(((item.precio_usd - item.costo_compra) / item.costo_compra) * 100) }}%)
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </div>
                  
                  <div v-else>
                    <div class="mb-3">
                      <strong>Información del producto preparado:</strong>
                    </div>
                    <v-list density="compact">
                      <v-list-item>
                        <v-list-item-title>Descripción:</v-list-item-title>
                        <v-list-item-subtitle>{{ item.descr_preparado || 'Sin descripción' }}</v-list-item-subtitle>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-title>Estado:</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-chip color="green" variant="tonal" size="small">
                            <v-icon start>mdi-chef-hat</v-icon>
                            Disponible para preparar
                          </v-chip>
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </div>
                </v-col>
              </v-row>

              <!-- Imagen ampliada si existe -->
              <v-row v-if="item.img" class="mt-4">
                <v-col cols="12">
                  <div class="mb-3">
                    <strong>Imagen del producto:</strong>
                  </div>
                  <v-img
                    :src="item.img"
                    :alt="item.nombre"
                    max-width="300"
                    max-height="200"
                    contain
                    class="rounded"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </td>
      </template>

      <!-- Template cuando no hay datos -->
      <template v-slot:no-data>
        <div class="text-center pa-4">
          <v-icon size="48" color="grey-lighten-1" class="mb-4">
            mdi-package-variant-off
          </v-icon>
          <div class="text-h6 mb-2">No hay productos registrados</div>
          <div class="text-subtitle-1 text-grey">
            Los productos aparecerán aquí cuando sean agregados al sistema.
          </div>
        </div>
  
  
      </template>
    </v-data-table>

    <!-- Diálogo de confirmación para eliminar -->
    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6 d-flex align-center">
          <v-icon color="error" class="me-2">mdi-delete</v-icon>
          Confirmar eliminación
        </v-card-title>
        
        <v-card-text>
          <div class="mb-4">
            ¿Estás seguro de que deseas eliminar el producto 
            <strong>"{{ productToDelete?.nombre }}"</strong>?
          </div>
          
          <v-alert type="warning" variant="tonal" class="mb-4">
            <v-alert-title>¡Atención!</v-alert-title>
            Esta acción no se puede deshacer. El producto será eliminado permanentemente del sistema.
          </v-alert>

          <div v-if="productToDelete?.tipo_producto === 'noPreparado' && productToDelete?.cant_actual > 0">
            <v-alert type="info" variant="tonal">
              <v-alert-title>Stock actual</v-alert-title>
              Este producto tiene {{ productToDelete.cant_actual }} {{ productToDelete.unidad_medida }} en stock.
            </v-alert>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn 
            variant="outlined"
            @click="showDeleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn 
            color="error"
            :loading="deletingProduct === productToDelete?.cod_producto"
            @click="deleteProduct"
          >
            <v-icon left>mdi-delete</v-icon>
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.product-list {
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

.text-success {
  color: rgb(var(--v-theme-success)) !important;
}
</style>