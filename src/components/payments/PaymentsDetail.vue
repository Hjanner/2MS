<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: Boolean,
  title: {
    type: String,
    default: 'Detalles del Pago'
  },
  paymentData: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:show']);

const metodoPagoConfig = {
  'efectivo_bs': { 
    label: 'Efectivo en Bolívares', 
    color: 'success', 
    icon: 'mdi-cash',
    currency: 'BS',
    description: 'Pago realizado en efectivo con moneda nacional'
  },
  'efectivo_usd': { 
    label: 'Efectivo en Dólares', 
    color: 'green-darken-2', 
    icon: 'mdi-currency-usd',
    currency: 'USD',
    description: 'Pago realizado en efectivo con moneda extranjera'
  },
  'pago_movil': { 
    label: 'Pago Móvil', 
    color: 'primary', 
    icon: 'mdi-cellphone',
    currency: 'BS',
    description: 'Transferencia bancaria desde dispositivo móvil'
  },
  'debito': { 
    label: 'Tarjeta de Débito', 
    color: 'orange', 
    icon: 'mdi-credit-card',
    currency: 'BS',
    description: 'Pago con tarjeta de débito bancaria'
  },
  'transferencia': { 
    label: 'Transferencia Bancaria', 
    color: 'purple', 
    icon: 'mdi-bank-transfer',
    currency: 'BS',
    description: 'Transferencia directa entre cuentas bancarias'
  }
};

const paymentConfig = computed(() => {
  if (!props.paymentData?.metodo_pago) return null;
  return metodoPagoConfig[props.paymentData.metodo_pago] || {
    label: props.paymentData.metodo_pago,
    color: 'default',
    icon: 'mdi-help-circle',
    currency: 'BS',
    description: 'Método de pago no reconocido'
  };
});

const formattedMonto = computed(() => {
  if (!props.paymentData?.monto) return 'N/A';
  
  try {
    const number = parseFloat(props.paymentData.monto);
    
    if (paymentConfig.value?.currency === 'USD') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(number);
    } else {
      return new Intl.NumberFormat('es-VE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(number) + ' BS';
    }
  } catch (error) {
    return props.paymentData.monto;
  }
});

const formattedFecha = computed(() => {
  if (!props.paymentData?.fecha_pago) return 'No especificado';
  
  try {
    const date = new Date(props.paymentData.fecha_pago);
    return date.toLocaleDateString('es-VE', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (error) {
    return props.paymentData.fecha_pago;
  }
});

const formattedTime = computed(() => {
  if (!props.paymentData?.fecha_pago) return 'No especificado';
  
  try {
    const date = new Date(props.paymentData.fecha_pago);
    return date.toLocaleTimeString('es-VE', {
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    return 'No disponible';
  }
});

const formattedTelefono = computed(() => {
  if (!props.paymentData?.num_tefl) return null;
  
  const telefono = props.paymentData.num_tefl;
  if (telefono.length === 11) {
    return `${telefono.substring(0, 4)}-${telefono.substring(4, 7)}-${telefono.substring(7)}`;
  }
  return telefono;
});

const isRecentPayment = computed(() => {
  if (!props.paymentData?.fecha_pago) return false;
  
  const paymentDate = new Date(props.paymentData.fecha_pago);
  const now = new Date();
  const diffHours = (now - paymentDate) / (1000 * 60 * 60);
  return diffHours <= 24;
});

const hasReference = computed(() => {
  return props.paymentData?.referencia && props.paymentData.referencia.trim() !== '';
});

const hasPhone = computed(() => {
  return props.paymentData?.num_tefl && props.paymentData.num_tefl.trim() !== '';
});

const hasNotes = computed(() => {
  return props.paymentData?.notas && props.paymentData.notas.trim() !== '';
});
</script>

<template>
  <v-dialog 
    :model-value="show" 
    @update:model-value="$emit('update:show', $event)"  
    max-width="650"
    persistent
  >
    <v-card v-if="paymentData">
      <v-card-title class="d-flex align-center bg-primary">
        <v-icon class="me-2" color="white">mdi-credit-card-multiple</v-icon>
        <span class="text-white">{{ title }}</span>
        <v-spacer></v-spacer>
        <v-chip
          v-if="isRecentPayment"
          color="success"
          variant="elevated"
          size="small"
        >
          <v-icon start size="small">mdi-clock-fast</v-icon>
          Reciente
        </v-chip>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Información principal del pago -->
        <v-row class="mb-4">
          <v-col cols="12">
            <v-card variant="tonal" :color="paymentConfig?.color">
              <v-card-text class="text-center">
                <v-icon 
                  :color="paymentConfig?.color" 
                  size="48"
                  class="mb-3"
                >
                  {{ paymentConfig?.icon }}
                </v-icon>
                <div class="text-h4 font-weight-bold mb-2">
                  {{ formattedMonto }}
                </div>
                <div class="text-h6 mb-1">
                  {{ paymentConfig?.label }}
                </div>
                <div class="text-caption text-medium-emphasis">
                  {{ paymentConfig?.description }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Detalles del pago -->
        <v-divider class="mb-4"></v-divider>
        
        <v-row>
          <v-col cols="12" sm="6">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="primary">mdi-identifier</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">ID del Pago</v-list-item-title>
              <v-list-item-subtitle>#{{ paymentData.id_pago }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" sm="6">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="secondary">mdi-shopping</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Venta Asociada</v-list-item-title>
              <v-list-item-subtitle>Venta #{{ paymentData.id_venta }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="8">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="info">mdi-calendar</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Fecha del Pago</v-list-item-title>
              <v-list-item-subtitle>{{ formattedFecha }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
          <v-col cols="12" sm="4">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="info">mdi-clock</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Hora</v-list-item-title>
              <v-list-item-subtitle>{{ formattedTime }}</v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <!-- Información adicional del método de pago -->
        <v-divider class="my-4"></v-divider>
        
        <div class="text-subtitle-1 font-weight-medium mb-3">
          <v-icon class="me-2">mdi-information-outline</v-icon>
          Información Adicional
        </div>

        <!-- Referencia (si existe) -->
        <v-row v-if="hasReference">
          <v-col cols="12">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="orange">mdi-bookmark-outline</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Referencia</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  color="orange"
                  variant="tonal"
                  size="small"
                  class="mt-1"
                >
                  {{ paymentData.referencia }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <!-- Teléfono (si existe) -->
        <v-row v-if="hasPhone">
          <v-col cols="12">
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="primary">mdi-phone</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Número de Teléfono</v-list-item-title>
              <v-list-item-subtitle>
                <v-chip
                  color="primary"
                  variant="tonal"
                  size="small"
                  class="mt-1"
                >
                  <v-icon start size="small">mdi-phone</v-icon>
                  {{ formattedTelefono }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <!-- Notas adicionales (si existen) -->
        <v-row v-if="hasNotes">
          <v-col cols="12">
            <v-divider class="mb-3"></v-divider>
            <v-list-item class="px-0">
              <template #prepend>
                <v-icon color="purple">mdi-note-text</v-icon>
              </template>
              <v-list-item-title class="font-weight-medium">Notas</v-list-item-title>
              <v-list-item-subtitle class="mt-1">
                <v-card variant="tonal" color="purple" class="pa-3">
                  <div class="text-body-2">{{ paymentData.notas }}</div>
                </v-card>
              </v-list-item-subtitle>
            </v-list-item>
          </v-col>
        </v-row>

        <!-- Información de estado y validez -->
        <v-divider class="my-4"></v-divider>
        
        <v-row>
          <v-col cols="12">
            <v-alert
              :type="isRecentPayment ? 'success' : 'info'"
              variant="tonal"
              class="mb-0"
            >
              <template #prepend>
                <v-icon>{{ isRecentPayment ? 'mdi-check-circle' : 'mdi-information' }}</v-icon>
              </template>
              <div class="d-flex justify-space-between align-center">
                <div>
                  <div class="font-weight-medium">
                    {{ isRecentPayment ? 'Pago Reciente' : 'Pago Registrado' }}
                  </div>
                  <div class="text-caption">
                    {{ isRecentPayment 
                      ? 'Este pago fue procesado en las últimas 24 horas' 
                      : 'Pago procesado y registrado correctamente en el sistema' 
                    }}
                  </div>
                </div>
                <v-icon 
                  :color="isRecentPayment ? 'success' : 'info'"
                  size="large"
                >
                  {{ isRecentPayment ? 'mdi-clock-fast' : 'mdi-check-circle' }}
                </v-icon>
              </div>
            </v-alert>
          </v-col>
        </v-row>
      </v-card-text>

      <!-- Acciones del modal -->
      <v-card-actions class="justify-end pa-4">
        <v-btn
          variant="outlined"
          @click="$emit('update:show', false)"
          class="me-2"
        >
          <v-icon start>mdi-close</v-icon>
          Cerrar
        </v-btn>
        
        <!-- <v-btn
          color="primary"
          variant="elevated"
          @click="() => { 
            if (navigator.share) {
              navigator.share({
                title: 'Detalles del Pago',
                text: `Pago #${paymentData.id_pago} - ${formattedMonto} - ${paymentConfig?.label}`
              });
            } else {
              navigator.clipboard.writeText(`Pago #${paymentData.id_pago} - ${formattedMonto} - ${paymentConfig?.label}`);
            }
          }"
        >
          <v-icon start>mdi-share</v-icon>
          Compartir
        </v-btn> -->
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.v-list-item {
  min-height: 48px;
}

.v-list-item-title {
  font-size: 0.875rem;
}

.v-list-item-subtitle {
  font-size: 0.75rem;
}

.text-h4 {
  line-height: 1.2;
}

.v-card-title {
  position: sticky;
  top: 0;
  z-index: 1;
}
</style>