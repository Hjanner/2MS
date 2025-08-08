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
        prepend-icon="mdi-cart"
        title="Productos"
        to="/Products"
      />

      <v-list-item
        link
        prepend-icon="mdi-account-group"
        title="Clientes"
        to="/Clients"
      />
    </v-list>
  </v-navigation-drawer>
</template>
