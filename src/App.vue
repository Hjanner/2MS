<script setup>
import { useSnackbar } from '@/composables/useSnackbar';

const { snackbar } = useSnackbar();
</script>

<template>
  <v-app>
    <Sidebar />
    <v-main>
      <router-view />
       <!-- Snackbar para notificaciones -->
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        timeout="3000"
        location="bottom right"
      >
        {{ snackbar.message }}
      </v-snackbar>
    </v-main>
  </v-app>
</template>
