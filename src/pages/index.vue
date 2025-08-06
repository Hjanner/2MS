<script setup>
  import { computed, provide } from 'vue'
  import { useCart } from '@/composables/useCart.js'
  import { useFetch } from '@/composables/useFetch.js'

  const { data, error } = useFetch('https://boringapi.com/api/v1/photos/random?num=10')
  const items = computed(() => data.value?.photos || [])

  const { cart, addItem, removeItem, updateQuantity } = useCart()
  provide('cartActions', { cart, addItem, removeItem, updateQuantity })

  const selectedItems = computed(() =>
    items.value
      .filter(i => cart[i.id])
      .map(i => ({ id: i.id, name: i.title, quantity: cart[i.id].quantity })),
  )
</script>

<template>
  <div class="home-page">
    <template v-if="error">
      <v-alert type="error">
        Error loading content
      </v-alert>
    </template>

    <template v-else-if="items.length > 0">
      <CardGrid :items />
    </template>

    <template v-else>
      <SkeletonGrid />
    </template>

    <Cart :selected-items="selectedItems" />
  </div>
</template>

<style scoped>
  .home-page {
    padding: 20px;
  }
</style>
