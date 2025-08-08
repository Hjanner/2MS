<script setup>
defineProps({
  loading: Boolean
});

defineEmits(['refresh']);
</script>

<template>
  <div class="d-flex justify-end mt-4">
    <v-btn
      color="primary"
      variant="outlined"
      @click="$emit('refresh')"
      :loading="loading"
    >
      <v-icon left>mdi-refresh</v-icon>
      Recargar Lista
    </v-btn>
  </div>
</template>