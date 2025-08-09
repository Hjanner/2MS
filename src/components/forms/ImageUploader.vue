<script setup>
import { ref, computed } from 'vue';
import { validateImage } from '@/utils/validators.js';

const props = defineProps({
  modelValue: String | File | null,
  errorMessages: Array,
  isEditing: Boolean
});

const emit = defineEmits(['update:modelValue']);

const fileInput = ref(null);
const imagePreview = ref(props.modelValue);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const validation = validateImage(file);
  if (validation !== true) {
    emit('update:modelValue', null);
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target.result;
    emit('update:modelValue', file);
  };
  reader.readAsDataURL(file);
};

const removeImage = () => {
  imagePreview.value = null;
  emit('update:modelValue', null);
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};
</script>

<template>
  <div class="mb-4">
    <h3 class="text-h6 mb-4 d-flex align-center">
      <v-icon class="me-2">mdi-camera</v-icon>
      Imagen del Producto
    </h3>

    <v-row>
      <v-col cols="12" md="8">
        <v-file-input
          ref="fileInput"
          @change="handleFileUpload"
          label="Seleccionar imagen"
          accept="image/*"
          prepend-icon="mdi-camera"
          :error-messages="errorMessages"
          :required="!isEditing"
          clearable
          @click:clear="removeImage"
          hint="Formatos soportados: JPG, PNG, GIF. Máximo 2MB"
          persistent-hint
        />
      </v-col>
      
      <v-col cols="12" md="4" v-if="imagePreview">
        <v-card variant="tonal">
          <v-card-subtitle>Vista previa</v-card-subtitle>
          <v-img
            :src="imagePreview"
            height="120"
            cover
            class="ma-2 rounded"
          />
          <v-card-actions>
            <v-btn
              color="error"
              size="small"
              variant="outlined"
              @click="removeImage"
              block
            >
              <v-icon left>mdi-delete</v-icon>
              Eliminar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>