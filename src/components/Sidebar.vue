<script setup>
  //
</script>

<template>
  <v-navigation-drawer
    expand-on-hover
    rail
  >
    <v-list>
      <v-list-item
        prepend-icon="mdi-alpha-m-box"
        subtitle="Sistema de gestión"
        title="MS2"
      />
    </v-list>

    <v-divider />

    <v-list nav>
      <v-list-item
        link
        prepend-icon="mdi-home"
        title="Inicio"
        value="inicio"
        to="/"
      />
    </v-list>

    <v-list nav>
      <v-list-item
        link
        prepend-icon="mdi-account-group"
        title="Clientes"
        value="clients"
        to="/clients"
      />
    </v-list>

    <v-list nav>
      <v-list-item
        link
        prepend-icon="mdi-food-variant"
        title="Productos"
        value="products"
        to="/products"
      />
    </v-list>

    <v-list nav>
      <v-list-item
        link
        prepend-icon="mdi-clipboard-list-outline"
        title="Inventario"
        value="inventory"
        to="/inventory"
      />
    </v-list>
  </v-navigation-drawer>
</template>
