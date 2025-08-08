<script setup>
  const { items } = defineProps({
    items: Array,
  })
</script>

<template>
  <v-container
    class="bg-grey-lighten-3"
    fluid
    min-height="100%"
  >
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
