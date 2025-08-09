<script setup>
const props = defineProps({
  modelValue: Object,
  errors: Object
});

const emit = defineEmits(['update:modelValue']);

const preparationData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});
</script>

<template>
  <div class="mb-6">
    <h3 class="text-h6 mb-4 d-flex align-center">
      <v-icon class="me-2" color="orange">mdi-chef-hat</v-icon>
      Información del Producto Preparado
    </h3>

    <v-textarea
      v-model="preparationData.descr"
      label="Descripción del producto"
      :error-messages="errors.descr"
      hint="Describe el producto preparado, ingredientes, etc."
      persistent-hint
      prepend-inner-icon="mdi-text"
      rows="3"
    />
  </div>
</template>