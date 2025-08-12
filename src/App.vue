<script setup>
  import { useSnackbar } from '@/composables/useSnackbar'
  import { useRoute } from 'vue-router'

  const { snackbar } = useSnackbar()

  const route = useRoute()
</script>

<template>
  <v-app>
    <Appbar />
    <Sidebar v-if="route.path !== '/Checkout'"/>
    <v-main>
      <router-view />
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        location="bottom right"
        timeout="3000"
      >
        {{ snackbar.message }}
      </v-snackbar>
    </v-main>
  </v-app>
</template>
