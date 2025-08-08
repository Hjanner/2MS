<script setup>
  import { computed, onUnmounted, provide } from 'vue'
  import { useCart } from '@/composables/useCart.js'
  import { useFetch } from '@/composables/useFetch.js'
  import { useSearchTerm } from '@/composables/useSearchTerm.js'

  const { data, error } = useFetch('http://127.0.0.1:8000/productos/')
  const items = computed(() => data.value || [])

  const { matchesSearchTerm, clearSearchTerm } = useSearchTerm()

  const filteredItems = computed(() =>
    items.value.filter(i => matchesSearchTerm(i.nombre)),
  )

  const {
    getCart,
    clearCart,
    addItem,
    removeItem,
    createItemQuantityModel,
    getItemTotal,
    getCartTotal,
  } = useCart()

  provide('cartActions', {
    getCart,
    clearCart,
    addItem,
    removeItem,
    createItemQuantityModel,
    getItemTotal,
    getCartTotal,
  })

  const selectedItems = computed(() =>
    items.value.filter(i => i.cod_producto in getCart()),
  )

  onUnmounted(() => {
    clearSearchTerm()
    clearCart()
  })
</script>

<template>
  <template v-if="error">
    Error
  </template>

  <template v-else-if="items.length > 0">
    <CardGrid :items="filteredItems" />
  </template>

  <template v-else>
    <SkeletonGrid />
  </template>

  <OrderSummary :selected-items="selectedItems" />
</template>
