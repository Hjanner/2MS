<script setup>
  import { useSnackbar } from '@/composables/useSnackbar'

  const { snackbar } = useSnackbar()
</script>

<template>
  <v-app>
    <Appbar />
    <Sidebar />
    <v-main>
      <router-view />
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        location="bottom right"
        text="{{ snackbar.message }}"
        timeout="3000"
      />
    </v-main>
  </v-app>
</template>
