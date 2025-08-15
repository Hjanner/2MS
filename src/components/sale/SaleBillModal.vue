<template>
  <v-dialog v-model="show" max-width="600">
    <v-card>
      <v-card-title class="text-h5">Factura de Venta</v-card-title>
      <v-card-text>
        <div class="mb-2"><b>Cliente:</b> {{ cliente ? cliente.nombre + ' (' + cliente.ci_cliente + ')' : venta?.ci_cliente }}</div>
        <div class="mb-2"><b>Fecha:</b> {{ venta?.fecha_hora ? new Date(venta.fecha_hora).toLocaleString() : '' }}</div>
        <v-divider class="my-2"/>
        <v-list density="compact">
          <v-list-item v-for="item in detalles" :key="item.cod_producto">
            <v-list-item-title>
              {{ item.cantidad_producto }} x {{ item.nombre || item.cod_producto }}
            </v-list-item-title>
            <v-list-item-subtitle>
              ${{ item.precio_unitario.toFixed(2) }} c/u
            </v-list-item-subtitle>
            <template #append>
              <span class="font-weight-bold">${{ (item.precio_unitario * item.cantidad_producto).toFixed(2) }}</span>
            </template>
          </v-list-item>
        </v-list>
        <v-divider class="my-2"/>
        <div><b>Total USD:</b> ${{ venta?.monto_total_usd?.toFixed(2) }}</div>
        <div><b>Total Bs:</b> Bs {{ venta?.monto_total_bs?.toFixed(2) }}</div>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn color="grey" variant="text" @click="close">Cancelar</v-btn>
        <v-btn color="success" @click="confirmarVenta">Confirmar Venta</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, watch, ref } from 'vue'
const props = defineProps({
  show: Boolean,
  venta: Object,
  detalles: Array,
  clientes: Array
})
const emit = defineEmits(['update:show', 'confirm'])
const show = ref(props.show)
watch(() => props.show, v => show.value = v)
function close() {
  emit('update:show', false)
}
function confirmarVenta() {
  emit('confirm')
  emit('update:show', false)  
}
const cliente = computed(() => {
  if (!props.venta || !props.clientes) return null
  return props.clientes.find(c => c.ci_cliente === props.venta.ci_cliente)
})
</script>
