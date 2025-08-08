<script setup>
import { defineProps } from 'vue';
import { formatCurrency } from '@/utils/formatters';

const props = defineProps({
  item: Object
});
</script>

<template>
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
              <v-list-item>
                <v-list-item-title>Proveedor (RIF):</v-list-item-title>
                <v-list-item-subtitle>{{ item.Rif || 'No especificado' }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Valor en inventario:</v-list-item-title>
                <v-list-item-subtitle class="font-weight-bold">
                  {{ formatCurrency(item.cant_actual * item.costo_compra) }}
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
                <v-list-item-subtitle>{{ item.descr_preparado || 'Sin descripción' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>