<script setup>
import { ref, computed, watch } from 'vue'
import { METODOS_PAGO } from '@/api/data'
import { getCurrentDate } from '@/utils/formatters'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  creditData: {
    type: Object,
    default: null
  },
  errors: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['submit', 'update:show'])

const dialog = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const form = ref(null)
const valid = ref(false)

const formData = ref({
  fecha_pago: getCurrentDate(),
  metodo_pago: '',
  monto_abono: '',
  referencia: '',
  num_tefl: '',
  comentarios: ''
})

const requiresReference = computed(() => {
  return ['pago_movil', 'transferencia', 'debito'].includes(formData.value.metodo_pago)
})

const maxMonto = computed(() => {
  return props.creditData ? props.creditData.monto_pendiente : 0
})

const nuevoMontoPagado = computed(() => {
  if (!props.creditData || !formData.value.monto_abono) return props.creditData?.monto_pagado || 0
  return props.creditData.monto_pagado + parseFloat(formData.value.monto_abono)
})

const nuevoMontoPendiente = computed(() => {
  if (!props.creditData) return 0
  return props.creditData.monto_total - nuevoMontoPagado.value
})

function getNewStatus() {
  if (!props.creditData || !formData.value.monto_abono) return props.creditData?.estado || 'Pendiente'
  
  const nuevoMonto = nuevoMontoPagado.value
  const total = props.creditData.monto_total
  
  if (nuevoMonto >= total) return 'Pagado'
  if (nuevoMonto === 0) return 'Pendiente'
  return 'Parcial'
}

function getNewStatusColor() {
  const status = getNewStatus()
  const colors = {
    'Pagado': 'success',
    'Pendiente': 'error',
    'Parcial': 'warning'
  }
  return colors[status] || 'grey'
}

function setQuickAmount(amount) {
  formData.value.monto_abono = Math.round(amount * 100) / 100
}

function resetForm() {
  formData.value = {
    fecha_pago: getCurrentDate(),
    metodo_pago: '',
    monto_abono: '',
    referencia: '',
    num_tefl: '',
    comentarios: ''
  }
  
  if (form.value) {
    form.value.resetValidation()
  }
}

function closeDialog() {
  dialog.value = false
  resetForm()
}

async function submitForm() {
  if (!form.value) return
  
  const formIsValid = await form.value.validate()
  if (!formIsValid.valid) return

  const paymentData = {
    ci_cliente: props.creditData.ci_cliente,
    fecha_credito: props.creditData.fecha_credito,
    fecha_pago: formData.value.fecha_pago,
    metodo_pago: formData.value.metodo_pago,
    monto_total: props.monto_total,
    monto_abono: parseFloat(formData.value.monto_abono),
    referencia: formData.value.referencia || null,
    num_tefl: formData.value.num_tefl || null,
    comentarios: formData.value.comentarios || null
  }  

  emit('submit', paymentData)
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  }).format(amount || 0)
}

</script>

<template>
  <v-dialog
    v-model="dialog"
    max-width="600px"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5 d-flex align-center">
        <v-icon class="mr-2" color="success">mdi-cash-plus</v-icon>
        Registrar Pago
      </v-card-title>

      <v-card-text>
        <!-- Información del crédito -->
        <v-card 
          v-if="creditData" 
          variant="outlined" 
          class="mb-4"
        >
          <v-card-title class="text-subtitle-1 pa-3">
            Información del Crédito
          </v-card-title>
          <v-card-text class="pt-0">
            <v-row dense>
              <v-col cols="6">
                <div class="text-caption text-grey">Cliente</div>
                <div class="font-weight-medium">
                  {{ creditData.cliente?.nombre || 'Cliente no encontrado' }}
                </div>
                <div class="text-caption">{{ creditData.ci_cliente }}</div>
              </v-col>
              <v-col cols="6">
                <div class="text-caption text-grey">Fecha del Crédito</div>
                <div class="font-weight-medium">{{ creditData.fecha_credito_formatted }}</div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">Monto Total</div>
                <div class="font-weight-medium text-h6">
                  {{ formatCurrency(creditData.monto_total) }}
                </div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">Ya Pagado</div>
                <div class="font-weight-medium text-success">
                  {{ formatCurrency(creditData.monto_pagado) }}
                </div>
              </v-col>
              <v-col cols="4">
                <div class="text-caption text-grey">Pendiente</div>
                <div class="font-weight-medium text-error">
                  {{ formatCurrency(creditData.monto_pendiente) }}
                </div>
              </v-col>
            </v-row>
            
            <!-- Barra de progreso -->
            <v-progress-linear
              :model-value="creditData.porcentaje_pagado"
              color="success"
              height="8"
              class="mt-3"
            />
            <div class="text-center text-caption mt-1">
              {{ creditData.porcentaje_pagado }}% pagado
            </div>
          </v-card-text>
        </v-card>

        <!-- Formulario de pago -->
        <v-form ref="form" v-model="valid">
          <v-container>
            <v-row>
              <!-- Fecha de pago -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.fecha_pago"
                  :error-messages="errors.fecha_pago"
                  label="Fecha de Pago"
                  type="date"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Fecha de pago es requerida']"
                />
              </v-col>

              <!-- Método de pago -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.metodo_pago"
                  :items="METODOS_PAGO"
                  :error-messages="errors.metodo_pago"
                  label="Método de Pago"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Método de pago es requerido']"
                />
              </v-col>

              <!-- Monto del abono -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.monto_abono"
                  :error-messages="errors.monto_abono"
                  label="Monto del Abono"
                  variant="outlined"
                  density="compact"
                  type="number"
                  step="0.01"
                  prefix="$"
                  :rules="[
                    v => !!v || 'Monto es requerido',
                    v => v > 0 || 'El monto debe ser mayor a 0',
                    v => v <= maxMonto || `El monto no puede ser mayor a ${formatCurrency(maxMonto)}`
                  ]"
                />
              </v-col>

              <!-- Botones de monto rápido -->
              <v-col cols="12" md="6">
                <div class="text-caption text-grey mb-2">Montos rápidos</div>
                <div class="d-flex flex-wrap gap-1">
                  <v-btn
                    size="x-small"
                    variant="outlined"
                    color="primary"
                    @click="setQuickAmount(maxMonto)"
                  >
                    Total
                  </v-btn>
                  <v-btn
                    size="x-small"
                    variant="outlined"
                    color="primary"
                    @click="setQuickAmount(maxMonto / 2)"
                  >
                    50%
                  </v-btn>
                  <v-btn
                    size="x-small"
                    variant="outlined"
                    color="primary"
                    @click="setQuickAmount(maxMonto / 4)"
                  >
                    25%
                  </v-btn>
                </div>
              </v-col>

              <!-- Referencia (condicional) -->
              <v-col
                v-if="requiresReference"
                cols="12"
              >
                <v-text-field
                  v-model="formData.referencia"
                  :error-messages="errors.referencia"
                  label="Referencia del Pago"
                  variant="outlined"
                  density="compact"
                  :rules="requiresReference ? [v => !!v || 'Referencia es requerida'] : []"
                  placeholder="Ej: Número de transferencia, referencia de pago móvil"
                />
              </v-col>

              <!-- Número de teléfono (para pago móvil) -->
              <v-col
                v-if="formData.metodo_pago === 'pago_movil'"
                cols="12"
              >
                <v-text-field
                  v-model="formData.num_tefl"
                  :error-messages="errors.num_tefl"
                  label="Número de Teléfono"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Número de teléfono es requerido para pago móvil']"
                  placeholder="04XX-XXXXXXX"
                />
              </v-col>

              <!-- Comentarios -->
              <v-col cols="12">
                <v-textarea
                  v-model="formData.comentarios"
                  :error-messages="errors.comentarios"
                  label="Comentarios (Opcional)"
                  variant="outlined"
                  density="compact"
                  rows="2"
                  placeholder="Información adicional sobre el pago..."
                />
              </v-col>
            </v-row>

            <!-- Resumen del pago -->
            <v-alert
              v-if="formData.monto_abono > 0"
              type="info"
              variant="tonal"
              class="mt-3"
            >
              <template #title>Resumen del Pago</template>
              <div class="mt-2">
                <div>Monto del abono: <strong>{{ formatCurrency(parseFloat(formData.monto_abono || 0)) }}</strong></div>
                <div>Nuevo saldo pagado: <strong>{{ formatCurrency(nuevoMontoPagado) }}</strong></div>
                <div>Saldo pendiente: <strong>{{ formatCurrency(nuevoMontoPendiente) }}</strong></div>
                <div>Estado resultante: 
                  <v-chip 
                    :color="getNewStatusColor()" 
                    size="small" 
                    variant="tonal"
                  >
                    {{ getNewStatus() }}
                  </v-chip>
                </div>
              </div>
            </v-alert>
          </v-container>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          color="grey"
          variant="text"
          @click="closeDialog"
        >
          Cancelar
        </v-btn>
        <v-btn
          color="success"
          variant="flat"
          :loading="loading"
          :disabled="!valid"
          @click="submitForm"
        >
          <v-icon start>mdi-cash-check</v-icon>
          Registrar Pago
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

