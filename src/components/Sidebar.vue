<script setup>
  //
</script>

<template>
  <v-navigation-drawer
    expand-on-hover
    rail
  >
    <v-list nav>
      <v-list-item
        link
        prepend-icon="mdi-home"
        title="Inicio"
        to="/"
      />

      <v-list-item
        link
        prepend-icon="mdi-clipboard-list-outline"
        title="Inventario"
        to="/Inventory"
      />

      <v-list-item
        link
        prepend-icon="mdi-account-group"
        title="Clientes"
        to="/Clients"
      />

      <v-list-item
        link
        prepend-icon="mdi-cart-variant"
        title="Compras"
        to="/Purchases"
      />

      <v-list-item
        link
        prepend-icon="mdi-cash-register"
        title="Ventas"
        to="/Sales"
      />

      <v-list-item
        link
        prepend-icon="mdi-credit-card-minus-outline"
        title="Deudas"
        to="/Debt"
      />

      <v-list-item
        link
        prepend-icon="mdi-truck-delivery-outline"
        title="Proveedores"
        to="/Supplier"
      />

      <v-list-item
        link
        prepend-icon="mdi-tag-multiple-outline"
        title="Categorías"
        to="/Category"
      />

      <v-list-item
        link
        prepend-icon="mdi-currency-usd"
        title="Tasas de Cambio"
        to="/ExchangeRate"
      />
    </v-list>


  </v-navigation-drawer>
</template>
