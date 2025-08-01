<script setup>
  import { computed, provide } from 'vue'
  import { useRouter } from 'vue-router'    //para rutas
  import { useCart } from '@/composables/useCart.js'
  import { useFetch } from '@/composables/useFetch.js'

  const router = useRouter()
  const { data, error } = useFetch('https://boringapi.com/api/v1/photos/random?num=10')
  const items = computed(() => data.value?.photos || [])

  const { cart, addItem, removeItem, updateQuantity } = useCart()
  provide('cartActions', { cart, addItem, removeItem, updateQuantity })

  const selectedItems = computed(() =>
    items.value
      .filter(i => cart[i.id])
      .map(i => ({ id: i.id, name: i.title, quantity: cart[i.id].quantity })),
  )

  function navigateToClients() {
    router.push('/client/clients')
  }

  function navigateToProducts() {
    router.push('/product/products')
  }
</script>

<template>
  <div class="home-page">
    <div class="d-flex justify-end mb-4">
      <v-btn
        color="primary"
        @click="navigateToClients"
        class="mr-2"
      >
        <v-icon left>mdi-account-group</v-icon>
        Manage Clients
      </v-btn>
      <v-btn
        color="primary"
        @click="navigateToProducts"
        class="mr-2"
      >
        <v-icon left>mdi-account-group</v-icon>
        Productos
      </v-btn>
    </div>

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
