<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getCurrentDate, getCurrentTimeStamp } from '@/utils/formatters'

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
  }
})

const emit = defineEmits(['submit', 'update:show'])

const dialog = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const form = ref(null)
const valid = ref(false)

const tiposVenta = [
  { title: 'De Contado', value: 'de_contado' },
  { title: 'Crédito', value: 'credito' }
]

const metodosPago = [
  { title: 'Efectivo Bs', value: 'efectivo_bs' },
  { title: 'Efectivo USD', value: 'efectivo_usd' },
  { title: 'Pago Móvil', value: 'pago_movil' },
  { title: 'Débito', value: 'debito' },
  { title: 'Transferencia', value: 'transferencia' }
]

const formData = ref({
  ci_cliente: '',
  tipo: 'de_contado',
  tasa_cambio: 1,
  fecha: getCurrentDate(),
  monto_total_usd: 0,
  monto_total_bs: 0,
  id_tasa: null // Para el modelo, pero usaremos tasa_cambio directamente
})

const pagoData = ref({
  monto: 0,
  fecha_pago: getCurrentDate(),
  metodo_pago: '',
  referencia: '',
  num_tefl: ''
})

const requiresReference = computed(() => {
  return ['pago_movil', 'transferencia'].includes(pagoData.value.metodo_pago)
})

function calcularTotales() {
  const totalUsd = props.productos.reduce((sum, item) => {
    return sum + (item.precio_usd * item.quantity)
  }, 0)
  
  formData.value.monto_total_usd = parseFloat(totalUsd.toFixed(2))
  
  if (formData.value.tasa_cambio > 0) {
    formData.value.monto_total_bs = parseFloat((totalUsd * formData.value.tasa_cambio).toFixed(2))
    pagoData.value.monto = formData.value.monto_total_bs
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
  
  // Preparar datos de venta según el modelo Pydantic
  const ventaData = {
    // No incluimos id_venta aquí, se generará automáticamente en el backend
    monto_total_bs: formData.value.monto_total_bs,
    fecha_hora: new Date().toISOString(),
    monto_total_usd: formData.value.monto_total_usd,
    tipo: formData.value.tipo,
    ci_cliente: formData.value.ci_cliente || null,
    id_tasa: null // Puedes agregar lógica para manejar tasas guardadas
  }

  // Preparar datos de detalles según el modelo DetalleVenta
  const detallesData = props.productos.map(item => ({
    // No incluimos id_venta aquí, se asignará automáticamente en el backend
    cod_producto: item.cod_producto,
    cantidad_producto: item.quantity,
    precio_unitario: item.precio_usd
  }))

  // Preparar datos de pago según el modelo Pago
  const pagoDataFinal = {
    // No incluimos id_venta aquí, se asignará automáticamente en el backend
    monto: pagoData.value.monto,
    fecha_pago: pagoData.value.fecha_pago,
    metodo_pago: pagoData.value.metodo_pago,
    referencia: pagoData.value.referencia || null,
    num_tefl: pagoData.value.num_tefl || null
  }

  const ventaCompleta = {
    venta: ventaData,
    detalles: detallesData,
    pago: pagoDataFinal
  }

  emit('submit', ventaCompleta)
  resetForm()
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
    // Reinicializar formulario cuando se abre
    formData.value.tasa_cambio = props.tasa_cambio || 1
    calcularTotales()
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
    max-width="800px"
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
              <!-- Información del Cliente -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.ci_cliente"
                  :error-messages="errors.ci_cliente"
                  label="CI del Cliente (Opcional)"
                  variant="outlined"
                  density="compact"
                />
              </v-col>

              <!-- Tipo de Venta -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.tipo"
                  :items="tiposVenta"
                  :error-messages="errors.tipo"
                  label="Tipo de Venta"
                  variant="outlined"
                  density="compact"
                  :rules="[v => !!v || 'Tipo de venta es requerido']"
                />
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
                    Productos en la Venta
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

              <!-- Información de Pago -->
              <v-col cols="12">
                <v-divider class="mb-4" />
                <h3 class="text-h6 mb-3">Información de Pago</h3>
              </v-col>

              <!-- Método de Pago -->
              <v-col cols="12" md="6">
                <v-select
                  v-model="pagoData.metodo_pago"
                  :items="metodosPago"
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

              <!-- Monto del Pago (automático pero editable) -->
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="pagoData.monto"
                  :error-messages="errors.monto"
                  label="Monto del Pago (Bs.)"
                  variant="outlined"
                  density="compact"
                  type="number"
                  step="0.01"
                  prefix="Bs."
                  :rules="[
                    v => !!v || 'Monto es requerido',
                    v => v > 0 || 'El monto debe ser mayor a 0'
                  ]"
                />
              </v-col>
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
          Registrar Venta
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

