<script setup>
  import { inject } from 'vue'

  const { selectedItems } = defineProps({
    selectedItems: Array,
  })

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
      >
        <template #subtitle>
          Bs. {{ (5 * cartActions.getItemQuantity(selectedItem.id)).toFixed(2) }}
        </template>

        <template #title>
          {{ selectedItem.name }}
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
            v-model="cartActions.createItemQuantityModel(selectedItem.id).value"
            control-variant="stacked"
            density="compact"
            :min="1"
            variant="outlined"
            width="80"
          />
        </template>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
