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
      />
    </v-list>
  </v-navigation-drawer>
</template>
