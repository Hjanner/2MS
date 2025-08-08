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
    <v-list nav>
      <v-list-item
        v-for="(item, key) in selectedItems"
        :key
        :class="key % 2 === 0 ? 'bg-grey-lighten-3' : ''"
        density="compact"
        lines="two"
      >
        <template #subtitle>
          <span class="text-subtitle-2">
            USD {{ cartActions.getItemTotal(item.cod_producto).toFixed(2) }}
          </span>
        </template>

        <template #title>
          <span class="text-subtitle-2">
            {{ item.nombre }}
          </span>
        </template>

        <template #prepend>
          <v-icon
            class="cursor-pointer"
            icon="mdi-delete-outline"
            @click="cartActions.removeItem(item.cod_producto)"
          />
        </template>

        <template #append>
          <v-number-input
            v-model="cartActions.createItemQuantityModel(item.cod_producto).value"
            control-variant="stacked"
            density="compact"
            hide-details
            :min="1"
            variant="outlined"
            width="80"
          />
        </template>
      </v-list-item>
    </v-list>

    <template #append>
      <v-container>
        <v-row class="mb-2 d-flex justify-space-between" dense>
          <span class="text-h6">
            Total
          </span>

          <span class="text-h6">
            USD {{ cartActions.getCartTotal().toFixed(2) }}
          </span>
        </v-row>

        <v-row dense>
          <v-col>
            <v-btn
              block
              color="primary"
              text="eliminar"
              variant="outlined"
              @click="cartActions.clearCart()"
            />
          </v-col>

          <v-col>
            <v-btn
              block
              color="primary"
              text="pagar"
              variant="flat"
            />
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-navigation-drawer>
</template>
