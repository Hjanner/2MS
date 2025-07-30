<script setup>
  import { inject } from 'vue'

  defineProps(['selectedItems'])

  const cartActions = inject('cartActions')
</script>

<template>
  <v-navigation-drawer
    location="right"
    :width="500"
  >
    <v-list>
      <v-list-item
        v-for="(selectedItem, key) in selectedItems"
        :key
        lines="two"
        :title="selectedItem.name"
      >
        <template #subtitle>
          <span>Bs. {{ (5 * selectedItem.quantity).toFixed(2) }}</span>
        </template>
        <template #prepend>
          <v-icon
            class="cursor-pointer"
            icon="mdi-delete-outline"
            @click="cartActions.removeItem(selectedItem.id)"
          />
        </template>
        <template #append>
          <v-number-input
            v-model="selectedItem.quantity"
            control-variant="stacked"
            density="compact"
            :min="1"
            variant="outlined"
            width="80"
            @update="newValue => cartActions.updateQuantity(selectedItem.id, newValue)"
          />
        </template>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
