<script setup>
  import { ref, computed, watch } from 'vue';
  
  const props = defineProps({
    data: {
      type: Array,
      required: true,
      default: () => []
    },
    searchFields: {
      type: Array,
      default: () => ['nombre'] // campos por defecto donde buscar
    },
    placeholder: {
      type: String,
      default: 'Buscar...'
    },
    showFieldFilter: {
      type: Boolean,
      default: false
    },
    resultText: {
      type: String,
      default: 'resultados'
    },
    debounceMs: {
      type: Number,
      default: 300
    }
  });
  
  const emit = defineEmits(['filtered', 'search']);
  
  const searchQuery = ref('');
  const selectedField = ref('all');
  
  const fieldOptions = computed(() => {
    const options = [
      { title: 'Todos los campos', value: 'all' }
    ];
    
    // Generar opciones basadas en searchFields
    props.searchFields.forEach(field => {
      const title = getFieldTitle(field);
      options.push({ title, value: field });
    });
    
    return options;
  });
  
  const filteredData = computed(() => {
    if (!searchQuery.value?.trim()) {
      return props.data;
    }
  
    const query = searchQuery.value.toLowerCase().trim();
    
    return props.data.filter(item => {
      if (selectedField.value === 'all') {
        // Buscar en todos los campos especificados
        return props.searchFields.some(field => {
          const value = getNestedValue(item, field);
          return String(value).toLowerCase().includes(query);
        });
      } else {
        // Buscar solo en el campo seleccionado
        const value = getNestedValue(item, selectedField.value);
        return String(value).toLowerCase().includes(query);
      }
    });
  });
  
  const filteredCount = computed(() => filteredData.value.length);
  const isFiltered = computed(() => searchQuery.value?.trim().length > 0);
  
  // Methods
  function getFieldTitle(field) {
    const fieldTitles = {
      'ci_cliente': 'C.I. Cliente',
      'nombre': 'Nombre',
      'tlf': 'Teléfono', 
      'depto_escuela': 'Depto/Escuela',
      // Agrega más mapeos según tus necesidades
    };
    return fieldTitles[field] || field.charAt(0).toUpperCase() + field.slice(1);
  }
  
  function getNestedValue(obj, path) {
    return path.split('.').reduce((o, p) => o?.[p], obj) ?? '';
  }

  let debounceTimer = null;
  
  function handleSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      emit('filtered', filteredData.value);
      emit('search', {
        query: searchQuery.value,
        field: selectedField.value,
        results: filteredData.value
      });
    }, props.debounceMs);
  }
  
  function clearSearch() {
    searchQuery.value = '';
    selectedField.value = 'all';
    emit('filtered', props.data);
    emit('search', {
      query: '',
      field: 'all',
      results: props.data
    });
  }
  
  // Watchers
  watch(() => props.data, () => {
    if (searchQuery.value?.trim()) {
      handleSearch();
    }
  }, { deep: true });
  
  // Emit initial data
  watch(() => props.data, (newData) => {
    if (!searchQuery.value?.trim()) {
      emit('filtered', newData);
    }
  }, { immediate: true });
</script>

<template>
    <div class="search-filter">
      <v-card flat class="mb-4">
        <v-card-text class="pb-2">
          <v-row align="center">
            <v-col cols="12" md="6">
              <v-text-field
                v-model="searchQuery"
                :placeholder="placeholder"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                clearable
                hide-details
                @input="handleSearch"
                @click:clear="clearSearch"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="4" v-if="showFieldFilter">
              <v-select
                v-model="selectedField"
                :items="fieldOptions"
                label="Buscar en"
                variant="outlined"
                density="compact"
                hide-details
                @update:model-value="handleSearch"
              ></v-select>
            </v-col>
            
            <v-col cols="12" md="2" class="d-flex justify-end">
              <v-chip 
                v-if="isFiltered"
                color="primary"
                variant="outlined"
                closable
                @click:close="clearSearch"
              >
                {{ filteredCount }} {{ resultText }}
              </v-chip>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
</template>
  

  
<style scoped>
  .search-filter {
    width: 100%;
  }
</style>


<!-- Para productos -->
<!-- <SearchFilter
  :data="productos"
  :search-fields="['codigo', 'nombre', 'categoria']"
  placeholder="Buscar productos..."
  result-text="productos"
  @filtered="handleFilteredProductos"
/> -->