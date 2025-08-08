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
    @click="cartActions.addItem(item.cod_producto, item.precio_usd)"
  >
    <v-img
      cover
      height="140"
      url="item.img"
    />

    <v-card-item
      class="text-center"
    >
      <span class="text-subtitle-2">
        {{ item.nombre }}
      </span>

      <br>

      <span class="text-grey-darken-2 text-subtitle-2">
        USD {{ item.precio_usd.toFixed(2) }}
      </span>
    </v-card-item>
  </v-card>
</template>
