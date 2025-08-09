<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: Boolean,
  title: String,
  loading: Boolean,
  mode: {
    type: String,
    default: 'add',
    validator: value => ['add', 'edit'].includes(value)
  }
});

const emit = defineEmits(['update:show', 'submit']);

const isEditing = computed(() => props.mode === 'edit');
</script>

<template>
  <v-dialog 
    :model-value="show" 
    @update:model-value="$emit('update:show', $event)"  
    max-width="700"
    persistent
  >
    <v-card>
      <v-card-title class="d-flex align-center">
        <v-icon class="me-2">
          {{ isEditing ? 'mdi-pencil' : 'mdi-plus' }}
        </v-icon>
        {{ title }}
        <slot name="title-append"></slot>
      </v-card-title>

      <v-card-text class="pa-6">
        <v-form @submit.prevent="$emit('submit')">
          <slot></slot>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-spacer></v-spacer>
        <v-btn 
          variant="outlined"
          @click="$emit('update:show', false)"
        >
          Cancelar
        </v-btn>

        <v-btn 
          color="primary"
          type="submit"
          :loading="loading"
        >
          <v-icon left>
            {{ isEditing ? 'mdi-content-save' : 'mdi-plus' }}
          </v-icon>
          {{ isEditing ? 'Actualizar' : 'Guardar' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>