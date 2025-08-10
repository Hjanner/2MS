<script setup>
import { ref, computed } from 'vue';
import { formatCurrency } from '@/utils/formatters';

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  show: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:show']);

const isOpen = computed({
  get() {
    return props.show;
  },
  set(value) {
    emit('update:show', value);
  }
});
</script>

<template>
  <v-dialog v-model="isOpen" max-width="800" persistent>
    <v-card>
      <v-card-title class="text-h6 d-flex align-center">
        <v-icon class="me-2">mdi-information</v-icon>
        Detalles de {{ product.nombre }}
        <v-spacer></v-spacer>
        <v-btn icon @click="isOpen = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <div class="mb-3">
              <strong>Información básica:</strong>
            </div>
            <v-list density="compact">
              <v-list-item>
                <v-list-item-title>Código: </v-list-item-title>
                <v-list-item-subtitle>{{ product.cod_producto }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Categoría:</v-list-item-title>
                <v-list-item-subtitle>{{ product.categoria_descr }} ({{ product.categoria_tipo }})</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Precio de venta:</v-list-item-title>
                <v-list-item-subtitle>{{ formatCurrency(product.precio_usd) }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          
          <v-col cols="12" md="6">
            <div v-if="product.tipo_producto === 'noPreparado'">
              <div class="mb-3">
                <strong>Información de inventario:</strong>
              </div>
              <v-list density="compact">
                <v-list-item>
                  <v-list-item-title>Stock actual:</v-list-item-title>
                  <v-list-item-subtitle>{{ product.cant_actual }} {{ product.unidad_medida }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Stock mínimo:</v-list-item-title>
                  <v-list-item-subtitle>{{ product.cant_min }} {{ product.unidad_medida }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Costo de compra:</v-list-item-title>
                  <v-list-item-subtitle>{{ formatCurrency(product.costo_compra) }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Proveedor (RIF):</v-list-item-title>
                  <v-list-item-subtitle>{{ product.Rif || 'No especificado' }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Valor en inventario:</v-list-item-title>
                  <v-list-item-subtitle class="font-weight-bold">
                    {{ formatCurrency(product.cant_actual * product.costo_compra) }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
            
            <div v-else>
              <div class="mb-3">
                <strong>Información de producto preparado:</strong>
              </div>
              <v-list density="compact">
                <v-list-item>
                  <v-list-item-title>Descripción:</v-list-item-title>
                  <v-list-item-subtitle>{{ product.descr_preparado || 'Sin descripción' }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="isOpen = false">Cerrar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>