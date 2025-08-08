<script setup>
  import { useRoute } from 'vue-router'
  import { useSearchTerm } from '@/composables/useSearchTerm.js'

  const { searchTerm, clearSearchTerm } = useSearchTerm()

  const route = useRoute()
</script>

<template>
  <v-app-bar
    class="border-b px-6"
    :elevation="0"
  >
    <template #prepend>
      <span class="text-h6 ">
        Sistema 2MS
      </span>

      <template v-if="route.path === '/'">
        <v-text-field
          v-model="searchTerm"
          append-inner-icon="mdi-magnify"
          bg-color="grey-lighten-3"
          class="px-6"
          clearable
          density="compact"
          hide-details
          label="Buscar producto"
          single-line
          variant="outlined"
          width="25vw"
          @click:clear="clearSearchTerm()"
        />
      </template>
    </template>
  </v-app-bar>
</template>
