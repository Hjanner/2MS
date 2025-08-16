<script setup>
  //
</script>

<template>
  <v-container>
    <v-row>
      <v-col
        v-for="n in 12"
        :key="n"
        cols="12"
        lg="3"
      >
        <v-skeleton-loader type="image, text@2" />
      </v-col>
    </v-row>
  </v-container>
</template>
