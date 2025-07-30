<script setup>
  defineProps(['items'])
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col
        v-for="(item, key) in items"
        :key
        cols="12"
        lg="3"
      >
        <Card :item />
      </v-col>
    </v-row>
  </v-container>
</template>
