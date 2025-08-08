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
        v-for="(item, key) in selectedItems"
        :key
        lines="two"
      >
        <template #subtitle>
          Bs. {{ cartActions.getItemSubtotal(item.cod_producto) }}
        </template>

        <template #title>
          {{ item.nombre }}
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
            Bs. {{ cartActions.getTotalPrice().toFixed(2) }}
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
