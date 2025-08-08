<script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  import { useFetch } from '@/composables/useFetch.js'
  import { useSearchTerm } from '@/composables/useSearchTerm.js'

  const { data, error } = useFetch('http://127.0.0.1:8000/dolar')
  const tasa = computed(() => data.value?.valor_usd_bs || '')

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

    <template v-if="error">
      <span class="text-grey-darken-1 text-subtitle-1">
        <b>Tasa no disponible</b>
      </span>
    </template>

    <template v-else-if="tasa">
      <span class="text-grey-darken-1 text-subtitle-1">
        <b>USD 1 = VED {{ tasa }}</b>
      </span>
    </template>

    <template v-else>
      <span class="text-grey-darken-1 text-subtitle-1">
        <b>Cargando tasa...</b>
      </span>
    </template>
  </v-app-bar>
</template>
