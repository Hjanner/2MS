<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { TIPOS_VENTA, METODOS_PAGO } from '@/api/data'
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
  title: {
    type: String,
    default: 'Registrar Venta'
  },
  productos: {
    type: Array,
    default: () => []
  },
  tasa_cambio: {
    type: Number,
    default: 1
  },
  errors: {
    type: Object,
    default: () => ({})
  },
  clientes: {
    type: Array,
    default: () => []
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
  ci_cliente: '',
  tipo: 'de_contado',
  tasa_cambio: 1,
  fecha: getCurrentDate(),
  monto_total_usd: 0,
  monto_total_bs: 0,
  id_tasa: null
})

const pagoData = ref({
  monto: 0,
  fecha_pago: getCurrentDate(),
  metodo_pago: '',
  referencia: '',
  num_tefl: ''
})

// Datos para crédito
const creditoData = ref({
  fecha_credito: getCurrentDate(),
  monto_inicial_pagado: 0
})

const esVentaCredito = computed(() => formData.value.tipo === 'credito')

const clienteSeleccionado = computed(() => {
  if (!formData.value.ci_cliente) return null
  return props.clientes.find(c => c.ci_cliente === formData.value.ci_cliente)
})

// Corregir la lógica de requiresReference
const requiresReference = computed(() => {
  const metodosQueRequierenReferencia = ['pago_movil', 'transferencia']
  
  if (esVentaCredito.value) {
    // Para venta a crédito, solo requiere referencia si hay pago inicial Y el método lo requiere
    return creditoData.value.monto_inicial_pagado > 0 && 
           metodosQueRequierenReferencia.includes(pagoData.value.metodo_pago)
  } else {
    // Para venta de contado, siempre verificar el método
    return metodosQueRequierenReferencia.includes(pagoData.value.metodo_pago)
  }
})

const clientesOptions = computed(() => {
  return props.clientes.map(cliente => ({
    title: `${cliente.nombre} (${cliente.ci_cliente})`,
    value: cliente.ci_cliente,
    subtitle: cliente.depto_escuela || ''
  }))
})

// Computed para el monto pendiente en crédito
const montoPendienteCredito = computed(() => {
  if (!esVentaCredito.value) return 0
  return Math.max(0, formData.value.monto_total_usd - creditoData.value.monto_inicial_pagado)
})

// Computed para el estado del crédito
const estadoCredito = computed(() => {
  if (!esVentaCredito.value) return ''
  
  const montoTotal = formData.value.monto_total_usd
  const montoPagado = creditoData.value.monto_inicial_pagado
  
  if (montoPagado >= montoTotal) {
    return 'Pagado'
  } else if (montoPagado > 0) {
    return 'Parcial'
  } else {
    return 'Pendiente'
  }
})

function calcularTotales() {
  const totalUsd = props.productos.reduce((sum, item) => {
    return sum + (item.precio_usd * item.quantity)
  }, 0)
  
  formData.value.monto_total_usd = parseFloat(totalUsd.toFixed(2))
  
  if (formData.value.tasa_cambio > 0) {
    formData.value.monto_total_bs = parseFloat((totalUsd * formData.value.tasa_cambio).toFixed(2))
    
    // Para venta de contado, el pago es el total
    if (!esVentaCredito.value) {
      pagoData.value.monto = formData.value.monto_total_bs
    }
  }
}

function resetForm() {
  formData.value = {
    ci_cliente: '',
    tipo: 'de_contado',
    tasa_cambio: props.tasa_cambio || 1,
    fecha: getCurrentDate(),
    monto_total_usd: 0,
    monto_total_bs: 0,
    id_tasa: null
  }
  
  pagoData.value = {
    monto: 0,
    fecha_pago: getCurrentDate(),
    metodo_pago: '',
    referencia: '',
    num_tefl: ''
  }

  creditoData.value = {
    fecha_credito: getCurrentDate(),
    monto_inicial_pagado: 0
  }
  
  if (form.value) {
    form.value.resetValidation()
  }
}

async function closeDialog() {
  dialog.value = false
  resetForm()
}

async function submitForm() {
  if (!form.value) return
  
  const formIsValid = await form.value.validate()
  if (!formIsValid.valid) return
  
  try {
    // Preparar datos de venta según el modelo Pydantic
    const ventaData = {
      monto_total_bs: formData.value.monto_total_bs,
      fecha_hora: new Date().toISOString(),
      monto_total_usd: formData.value.monto_total_usd,
      tipo: formData.value.tipo,
      ci_cliente: formData.value.ci_cliente || null,
      id_tasa: null
    }

    // Preparar datos de detalles según el modelo DetalleVenta
    const detallesData = props.productos.map(item => ({
      cod_producto: item.cod_producto,
      cantidad_producto: item.quantity,
      precio_unitario: item.precio_usd
    }))

    // Usar el payload unificado
    let ventaCompleta = {
      venta: ventaData,
      detalles: detallesData,
      tipo_transaccion: formData.value.tipo
    }

    if (esVentaCredito.value) {
      // Para venta a crédito, preparar datos del crédito
      ventaCompleta.credito = {
        ci_cliente: formData.value.ci_cliente,
        fecha_credito: creditoData.value.fecha_credito,
        fecha_ultimo_abono: creditoData.value.monto_inicial_pagado > 0 
          ? pagoData.value.fecha_pago 
          : null,
        monto_total: formData.value.monto_total_usd,
        monto_pagado: creditoData.value.monto_inicial_pagado,
        estado: estadoCredito.value
      }

      // Si hay pago inicial en crédito, incluir datos del pago
      if (creditoData.value.monto_inicial_pagado > 0) {
        ventaCompleta.pago = {
          monto: parseFloat((creditoData.value.monto_inicial_pagado * formData.value.tasa_cambio).toFixed(2)),
          fecha_pago: pagoData.value.fecha_pago,
          metodo_pago: pagoData.value.metodo_pago,
          referencia: pagoData.value.referencia || null,
          num_tefl: pagoData.value.num_tefl || null
        }
      }
    } else {
      // Para venta de contado, incluir datos del pago completo
      ventaCompleta.pago = {
        monto: pagoData.value.monto,
        fecha_pago: pagoData.value.fecha_pago,
        metodo_pago: pagoData.value.metodo_pago,
        referencia: pagoData.value.referencia || null,
        num_tefl: pagoData.value.num_tefl || null
      }
    }

    console.log('Enviando venta:', ventaCompleta)
    emit('submit', ventaCompleta)
    resetForm()
  } catch (error) {
    console.error('Error al preparar datos de venta:', error)
  }
}

// Watchers
watch(() => props.productos, calcularTotales, { deep: true, immediate: true })

watch(() => props.tasa_cambio, (newTasa) => {
  if (newTasa && newTasa > 0) {
    formData.value.tasa_cambio = newTasa
    calcularTotales()
  }
}, { immediate: true })

watch(() => props.show, (newVal) => {
  if (newVal) {
    formData.value.tasa_cambio = props.tasa_cambio || 1
    calcularTotales()
  }
})

watch(() => formData.value.tipo, (newTipo) => {
  if (newTipo === 'credito') {
    // Reset pago data when switching to credit
    pagoData.value.monto = 0
    pagoData.value.metodo_pago = ''
    pagoData.value.referencia = ''
    pagoData.value.num_tefl = ''
    creditoData.value.monto_inicial_pagado = 0
  } else {
    // Set full amount as payment for cash sales
    pagoData.value.monto = formData.value.monto_total_bs
    // Reset credit data
    creditoData.value.monto_inicial_pagado = 0
  }
})

watch(() => creditoData.value.monto_inicial_pagado, (newAmount) => {
  if (esVentaCredito.value && newAmount >= 0) {
    pagoData.value.monto = parseFloat((newAmount * formData.value.tasa_cambio).toFixed(2))
    
    // Si no hay pago inicial, limpiar datos de pago
    if (newAmount === 0) {
      pagoData.value.metodo_pago = ''
      pagoData.value.referencia = ''
      pagoData.value.num_tefl = ''
    }
  }
})

// Watch para limpiar campos condicionales cuando cambia el método de pago
watch(() => pagoData.value.metodo_pago, (newMethod) => {
  // Limpiar campos específicos cuando cambia el método
  if (newMethod !== 'pago_movil') {
    pagoData.value.num_tefl = ''
  }
  if (!['pago_movil', 'transferencia'].includes(newMethod)) {
    pagoData.value.referencia = ''
  }
})

onMounted(() => {
  formData.value.tasa_cambio = props.tasa_cambio || 1
  calcularTotales()
})
</script>

<template>
  <v-dialog
    v-model="dialog"
    max-width="900px"
    persistent
  >
    <v-card>
      <v-card-title class="text-h5">
        {{ title }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-container>
            <v-row>
              <!-- Tipo de Venta -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.tipo"
                  :items="TIPOS_VENTA"
                  :error-messages="errors.tipo"
                  label="Tipo de Venta"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Tipo de venta es requerido']"
                />
              </v-col>

              <!-- Cliente (obligatorio para crédito, opcional para contado) -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.ci_cliente"
                  :items="clientesOptions"
                  :error-messages="errors.ci_cliente"
                  :label="esVentaCredito ? 'Cliente (Requerido)' : 'Cliente (Opcional)'"
                  variant="outlined"
                  density="compact"
                  clearable
                  :rules="esVentaCredito ? [v => !!v || 'Cliente es requerido para venta a crédito'] : []"
                />
              </v-col>

              <!-- Información del cliente seleccionado -->
              <v-col v-if="clienteSeleccionado" cols="12">
                <v-alert type="info" variant="tonal">
                  <template #title>Cliente Seleccionado</template>
                  <div class="mt-1">
                    <strong>{{ clienteSeleccionado.nombre }}</strong> - {{ clienteSeleccionado.ci_cliente }}
                    <div v-if="clienteSeleccionado.depto_escuela" class="text-caption">
                      {{ clienteSeleccionado.depto_escuela }}
                    </div>
                    <div v-if="clienteSeleccionado.tlf" class="text-caption">
                      Teléfono: {{ clienteSeleccionado.tlf }}
                    </div>
                  </div>
                </v-alert>
              </v-col>

              <!-- Tasa de Cambio -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.tasa_cambio"
                  :error-messages="errors.tasa_cambio"
                  label="Tasa de Cambio (Bs. por USD)"
                  variant="outlined"
                  density="compact"
                  type="number"
                  step="0.0001"
                  :rules="[
                    v => !!v || 'Tasa de cambio es requerida',
                    v => v > 0 || 'La tasa debe ser mayor a 0'
                  ]"
                  @update:model-value="calcularTotales"
                />
              </v-col>

              <!-- Fecha -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.fecha"
                  :error-messages="errors.fecha"
                  label="Fecha"
                  type="date"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Fecha es requerida']"
                />
              </v-col>

              <!-- Resumen de productos -->
              <v-col cols="12">
                <v-card variant="outlined">
                  <v-card-title class="text-subtitle-1">
                    Productos en la Venta ({{ productos.length }} {{ productos.length === 1 ? 'producto' : 'productos' }})
                  </v-card-title>
                  <v-card-text>
                    <v-list density="compact">
                      <v-list-item
                        v-for="item in productos"
                        :key="item.cod_producto"
                        :title="item.nombre"
                        :subtitle="`Cantidad: ${item.quantity} | Precio: $${item.precio_usd.toFixed(2)}`"
                      >
                        <template #append>
                          <span class="text-body-2 font-weight-bold">
                            ${{ (item.precio_usd * item.quantity).toFixed(2) }}
                          </span>
                        </template>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>

              <!-- Totales -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.monto_total_usd"
                  label="Total USD"
                  variant="outlined"
                  density="compact"
                  readonly
                  prefix="$"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.monto_total_bs"
                  label="Total Bs."
                  variant="outlined"
                  density="compact"
                  readonly
                  prefix="Bs."
                />
              </v-col>

              <!-- Sección específica para crédito -->
              <template v-if="esVentaCredito">
                <v-col cols="12">
                  <v-divider class="mb-4" />
                  <h3 class="text-h6 mb-3">
                    <v-icon class="mr-2" color="warning">mdi-credit-card-clock</v-icon>
                    Información del Crédito
                  </h3>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="creditoData.fecha_credito"
                    :error-messages="errors.fecha_credito"
                    label="Fecha del Crédito"
                    type="date"
                    variant="outlined"
                    density="compact"
                    :rules="[v => !!v || 'Fecha del crédito es requerida']"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="creditoData.monto_inicial_pagado"
                    :error-messages="errors.monto_inicial_pagado"
                    label="Pago Inicial (USD - Opcional)"
                    variant="outlined"
                    density="compact"
                    type="number"
                    step="0.01"
                    min="0"
                    :max="formData.monto_total_usd"
                    prefix="$"
                    :rules="[
                      v => v >= 0 || 'El monto no puede ser negativo',
                      v => v <= formData.monto_total_usd || `No puede ser mayor al total ($${formData.monto_total_usd})`
                    ]"
                    hint="Dejar en 0 si no hay pago inicial"
                  />
                </v-col>

                <!-- Mostrar información del crédito -->
                <!-- <v-col cols="12">
                  <v-alert 
                    variant="tonal"
                  >
                    <template #title>Resumen del Crédito</template>
                    <div class="mt-1">
                      <div>Monto total del crédito: <strong>${{ formData.monto_total_usd.toFixed(2) }} USD</strong></div>
                      <div>Pago inicial: <strong>${{ creditoData.monto_inicial_pagado.toFixed(2) }} USD</strong>
                        <span v-if="creditoData.monto_inicial_pagado > 0">
                          (Bs. {{ (creditoData.monto_inicial_pagado * formData.tasa_cambio).toFixed(2) }})
                        </span>
                      </div>
                      <div>Monto pendiente: <strong>${{ montoPendienteCredito.toFixed(2) }} USD</strong></div>
                      <div>Estado: <strong>{{ estadoCredito }}</strong></div>
                    </div>
                  </v-alert>
                </v-col> -->
              </template>

              <!-- Información de Pago (para contado o pago inicial en crédito) -->
              <template v-if="!esVentaCredito || creditoData.monto_inicial_pagado > 0">
                <v-col cols="12">
                  <v-divider class="mb-4" />
                  <h3 class="text-h6 mb-3">
                    <v-icon class="mr-2" color="success">mdi-cash</v-icon>
                    {{ esVentaCredito ? 'Información del Pago Inicial' : 'Información de Pago' }}
                  </h3>
                </v-col>

                <!-- Método de Pago -->
                <v-col cols="12" md="6">
                  <v-select
                    v-model="pagoData.metodo_pago"
                    :items="METODOS_PAGO"
                    :error-messages="errors.metodo_pago"
                    label="Método de Pago"
                    variant="outlined"
                    density="compact"
                    :rules="[v => !!v || 'Método de pago es requerido']"
                  />
                </v-col>

                <!-- Fecha de Pago -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="pagoData.fecha_pago"
                    :error-messages="errors.fecha_pago"
                    label="Fecha de Pago"
                    type="date"
                    variant="outlined"
                    density="compact"
                    :rules="[v => !!v || 'Fecha de pago es requerida']"
                  />
                </v-col>

                <!-- Referencia (condicional) -->
                <v-col
                  v-if="requiresReference"
                  cols="12"
                  md="6"
                >
                  <v-text-field
                    v-model="pagoData.referencia"
                    :error-messages="errors.referencia"
                    label="Referencia"
                    variant="outlined"
                    density="compact"
                    :rules="requiresReference ? [v => !!v || 'Referencia es requerida'] : []"
                  />
                </v-col>

                <!-- Número de Teléfono (para pago móvil) -->
                <v-col
                  v-if="pagoData.metodo_pago === 'pago_movil'"
                  cols="12"
                  md="6"
                >
                  <v-text-field
                    v-model="pagoData.num_tefl"
                    :error-messages="errors.num_tefl"
                    label="Número de Teléfono"
                    variant="outlined"
                    density="compact"
                    :rules="[v => !!v || 'Número de teléfono es requerido para pago móvil']"
                  />
                </v-col>

                <!-- Monto del Pago (automático pero visible) -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="pagoData.monto"
                    :label="esVentaCredito ? 'Monto del Pago Inicial (Bs.)' : 'Monto del Pago (Bs.)'"
                    variant="outlined"
                    density="compact"
                    readonly
                    prefix="Bs."
                  />
                </v-col>
              </template>
            </v-row>
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
          color="primary"
          variant="flat"
          :loading="loading"
          :disabled="!valid"
          @click="submitForm"
        >
          <v-icon start>
            {{ esVentaCredito ? 'mdi-credit-card-plus' : 'mdi-cash-register' }}
          </v-icon>
          {{ esVentaCredito ? 'Registrar Crédito' : 'Registrar Venta' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>