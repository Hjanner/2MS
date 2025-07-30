<script setup>
  import { inject } from 'vue'

  defineProps(['item'])

  const cartActions = inject('cartActions')
</script>

<template>
  <v-card
    v-ripple
    class="mx-auto cursor-pointer"
    width="100%"
    @click="cartActions.addItem(item.id)"
  >
    <v-img
      cover
      height="140"
      :src="item.url"
    />

    <v-card-item class="text-center">
      <v-card-title>
        Producto
      </v-card-title>

      <v-card-subtitle>
        Precio
      </v-card-subtitle>
    </v-card-item>
  </v-card>
</template>
