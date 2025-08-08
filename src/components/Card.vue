<script setup>
  import { inject } from 'vue'

  const { item } = defineProps({
    item: Object,
  })

  const cartActions = inject('cartActions')
</script>

<template>
  <v-card
    density="compact"
    link
    variant="tonal"
    @click="cartActions.addItem(item.cod_producto, item.precio)"
  >
    <v-img
      cover
      height="140"
    />

    <v-card-item
      class="text-center"
    >
      <v-card-title>
        {{ item.nombre }}
      </v-card-title>

      <v-card-subtitle>
        <b>Bs. {{ item.precio }}</b>
      </v-card-subtitle>
    </v-card-item>
  </v-card>
</template>
