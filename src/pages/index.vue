<script setup>
  import { computed, onUnmounted, provide } from 'vue'
  import { useCart } from '@/composables/useCart.js'
  import { useFetch } from '@/composables/useFetch.js'
  import { useSearchTerm } from '@/composables/useSearchTerm.js'

  /**
   * @typedef {object} FetchResult
   * @property {Array<Object>} data
   * @property {string|null} error
   */

  /** @type {FetchResult} */
  const { data, error } = useFetch('http://127.0.0.1:8000/productos/')

  /**
   * @typedef {object} Producto
   * @property {string} cod_producto
   * @property {string} nombre
   * @property {number} precio_usd
   * @property {number} id_categoria
   * @property {string} img
   */

  /** @type {import('vue').ComputedRef<Producto[]>} */
  const items = computed(() => data.value || [])

  const { searchTerm, clearSearchTerm } = useSearchTerm()

  const filteredItems = computed(() => {
    const searchTermString = searchTerm.value.toString().toLowerCase() || ''

    return items.value.filter(i => i.nombre.toString().toLowerCase().includes(searchTermString))
  })

  const {
    getCart,
    clearCart,
    addItem,
    removeItem,
    createItemQuantityModel,
    getItemSubtotal,
    getTotalPrice,
  } = useCart()

  provide('cartActions', {
    getCart,
    clearCart,
    addItem,
    removeItem,
    createItemQuantityModel,
    getItemSubtotal,
    getTotalPrice,
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
