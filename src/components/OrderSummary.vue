<script setup>
import { inject, toRefs, ref, onMounted, computed, watch } from 'vue'
import SaleForm from '@/components/sale/SaleForm.vue'
import SaleBillModal from '@/components/sale/SaleBillModal.vue'
import LowStockAlert from '@/components/inventory/LowStockAlert.vue'
import { useSnackbar } from '@/composables/useSnackbar'
import { useStockValidation } from '@/composables/useStockValidation'
import api from '@/api/api'

const props = defineProps({
  selectedItems: {
    type: Array,
    default: () => [],
  },
})

const { selectedItems } = toRefs(props)
const cartActions = inject('cartActions')
const { showSnackbar } = useSnackbar()

// Usar el composable de validación de stock
const {
  lowStockProducts,
  outOfStockProducts,
  fetchProductosStock,
  validateCartStock,
  getProductStockStatus,
  canProceedWithSale,
  getCartStockSummary
} = useStockValidation()

// Estados para el diálogo de venta y factura
const showSaleDialog = ref(false)
const submittingSale = ref(false)
const saleErrors = ref({})
const tasas = ref(0)
const clientes = ref([])
const showFactura = ref(false)
const facturaVenta = ref(null)
const facturaDetalles = ref([])

// Estados para validación de stock
const showStockAlert = ref(false)
const currentStockValidation = ref({ errors: [], warnings: [], hasErrors: false })

// Computed para el total en bolívares
const totalBolivares = computed(() => {
  return (cartActions.getCartTotal() * tasas.value).toFixed(2)
})

// Computed para verificar si el carrito tiene items
const hasItems = computed(() => {
  return selectedItems.value.length > 0
})

// Computed para determinar si se puede proceder con la venta
const canProceedSale = computed(() => {
  return !currentStockValidation.value.hasErrors
})

// Watch para validar stock cuando cambie el carrito
watch(selectedItems, (newItems) => {
  if (newItems.length > 0) {
    currentStockValidation.value = validateCartStock(newItems)
    
    // Mostrar alert si hay errores críticos
    if (currentStockValidation.value.hasErrors) {
      showStockAlert.value = true
    }
  } else {
    currentStockValidation.value = { errors: [], warnings: [], hasErrors: false }
    showStockAlert.value = false
  }
}, { deep: true })

async function fetchClientes() {
  try {
    const response = await api.get('/clientes')
    clientes.value = response.data
    console.log('Clientes cargados:', clientes.value.length)
  } catch (error) {
    console.error('Error al cargar clientes:', error)
    showSnackbar('Error al cargar la lista de clientes', 'error')
  } 
}

// Función para obtener tasas de cambio
async function fetchTasas() {
  try {
    const response = await api.get('/tasas_cambio/ultima_tasa/')
    tasas.value = response.data.valor_usd_bs
    console.log('Tasa obtenida:', tasas.value)
  } catch (error) {
    console.error('Error al cargar tasas:', error)
    showSnackbar('Error al cargar las tasas de cambio', 'error')
    // Valor por defecto si falla
    tasas.value = 36.50
  }
}

// Función para manejar el pago con validación de stock
async function handlerPay() {
  if (selectedItems.value.length === 0) {
    showSnackbar('No hay productos en el carrito', 'warning')
    return
  }
  
  try {
    // Cargar datos necesarios
    await Promise.all([fetchTasas(), fetchClientes(), fetchProductosStock()])
    
    // Validar stock y mostrar notificaciones
    const canProceed = canProceedWithSale(selectedItems.value)
    
    if (canProceed) {
      showSaleDialog.value = true
    } else {
      showSnackbar('No se puede proceder con la venta debido a problemas de stock', 'error')
    }
  } catch (error) {
    console.error('Error al cargar datos:', error)
    showSnackbar('Error al cargar datos necesarios para la venta', 'error')
  }
}

// Función para manejar el envío de la venta (con validación final)
async function handleSubmitSale(ventaCompleta) {
  // Validación final antes de enviar
  const finalValidation = validateCartStock(selectedItems.value)
  
  if (finalValidation.hasErrors) {
    showSnackbar('No se puede completar la venta: Stock insuficiente', 'error')
    return
  }
  
  submittingSale.value = true
  saleErrors.value = {}
  try {
    let response
    if (ventaCompleta.tipo_transaccion === 'credito') {
      response = await api.post('/ventas/registrar_credito', {
        venta: ventaCompleta.venta,
        detalles: ventaCompleta.detalles,
        credito: ventaCompleta.credito,
        pago_inicial: ventaCompleta.pago
      })
      showSnackbar('Venta a crédito registrada correctamente', 'success')
    } else {
      response = await api.post('/ventas/registrar', {
        venta: ventaCompleta.venta,
        detalles: ventaCompleta.detalles,
        pago: ventaCompleta.pago
      })
      showSnackbar('Venta registrada correctamente', 'success')
    }
    
    // Mostrar factura
    facturaVenta.value = { ...ventaCompleta.venta, ...response.data }
    facturaDetalles.value = ventaCompleta.detalles.map(det => {
      const prod = selectedItems.value.find(p => p.cod_producto === det.cod_producto)
      return { ...det, nombre: prod ? prod.nombre : det.cod_producto }
    })
    showFactura.value = true
    
    // Cerrar diálogo y limpiar carrito
    showSaleDialog.value = false
    cartActions.clearCart()
    
    // Actualizar stock después de la venta exitosa
    await fetchProductosStock()
    
    // Verificar si hay nuevos productos en stock bajo después de la venta
    setTimeout(() => {
      if (lowStockProducts.value.length > 0) {
        showSnackbar(`Atención: ${lowStockProducts.value.length} productos han quedado en stock bajo`, 'info')
      }
    }, 1000)
    
  } catch (error) {
    console.error('Error al registrar la venta:', error)
    if (error.response?.data?.detail) {
      if (typeof error.response.data.detail === 'string') {
        showSnackbar(error.response.data.detail, 'error')
      } else if (Array.isArray(error.response.data.detail)) {
        const errorMessages = error.response.data.detail.map(err => err.msg).join(', ')
        showSnackbar(errorMessages, 'error')
      }
    } else {
      showSnackbar('Error al registrar la venta', 'error')
    }
    handleApiError(error, saleErrors)
  } finally {
    submittingSale.value = false
  }
}

// Función auxiliar para manejar errores de API
function handleApiError(error, errorRef) {
  console.log('Error de API:', error)
  
  if (error.response) {
    const backendErrors = {}

    if (error.response?.data?.detail) {
      const errorDetail = error.response.data.detail

      if (Array.isArray(errorDetail)) {
        errorDetail.forEach(err => {
          if (err.loc && err.loc.length > 1) {
            backendErrors[err.loc[1]] = err.msg
          }
        })
      } else if (typeof errorDetail === 'object' && errorDetail.field) {
        backendErrors[errorDetail.field] = errorDetail.message
      } else if (typeof errorDetail === 'string') {
        backendErrors.general = errorDetail
      }

      errorRef.value = backendErrors
    } else {
      const message = error.response.data?.message || `Error del servidor: ${error.response.status}`
      showSnackbar(message, 'error')
    }
  } else if (error.request) {
    console.log('Error de red:', error.request)
    showSnackbar('Error de conexión con el servidor', 'error')
  } else {
    console.log('Error:', error.message)
    showSnackbar('Error inesperado: ' + error.message, 'error')
  }
}

async function closeSaleDialog() {
  showSaleDialog.value = false
  saleErrors.value = {}
}

// Función para formatear precio
function formatPrice(price) {
  return parseFloat(price).toFixed(2)
}

// Función para obtener el total de un item
function getItemTotal(item) {
  return item.precio_usd * item.quantity
}

onMounted(() => {
  fetchTasas()
  fetchProductosStock()
})
</script>

<template>
  <v-navigation-drawer
    location="right"
    :width="500"
    permanent
  >
    <!-- Alertas de stock bajo -->
    <LowStockAlert 
      :low-stock-products="lowStockProducts"
      :out-of-stock-products="outOfStockProducts"
    />

    <!-- Alert de errores de stock durante validación -->
    <v-alert
      v-if="showStockAlert && currentStockValidation.hasErrors"
      type="error"
      variant="tonal"
      closable
      class="ma-3"
      @click:close="showStockAlert = false"
    >
      <v-alert-title>
        <v-icon>mdi-alert-circle</v-icon>
        No se puede completar la venta
      </v-alert-title>
      <div class="mt-2">
        <div v-for="error in currentStockValidation.errors" :key="error.cod_producto" class="mb-1">
          • {{ error.mensaje }}
        </div>
      </div>
    </v-alert>

    <!-- Alert de advertencias de stock -->
    <v-alert
      v-if="currentStockValidation.hasWarnings && !currentStockValidation.hasErrors"
      type="warning"
      variant="tonal"
      density="compact"
      class="ma-3"
    >
      <div class="d-flex align-center">
        <v-icon size="small" class="mr-2">mdi-information</v-icon>
        <span class="text-caption">
          {{ currentStockValidation.warnings.length }} producto(s) con advertencias de stock
        </span>
      </div>
    </v-alert>

    <!-- Contenido del carrito -->
    <template v-if="hasItems">
      <v-list nav class="py-0">
        <v-list-item
          v-for="(item, index) in selectedItems"
          :key="item.cod_producto"
          :class="[
            index % 2 === 0 ? 'bg-grey-lighten-4' : '',
            getProductStockStatus(item).status === 'insufficient' ? 'border-error' : ''
          ]"
          density="compact"
          lines="three"
          class="px-3 py-2"
        >
          <template #prepend>
            <v-btn
              icon="mdi-delete-outline"
              variant="text"
              size="small"
              color="error"
              @click="cartActions.removeItem(item.cod_producto)"
            >
            </v-btn>
          </template>

          <template #title>
            <div class="text-subtitle-1 font-weight-medium">
              {{ item.nombre }}
            </div>
            <div> 
              <span class="text-caption text-medium-emphasis">
                ${{ formatPrice(item.precio_usd) }} c/u
              </span>
            </div>
            
            <!-- Indicador de estado de stock -->
            <div class="mt-1">
              <v-chip
                :color="getProductStockStatus(item).color"
                size="x-small"
                variant="tonal"
                :prepend-icon="getProductStockStatus(item).icon"
              >
                {{ getProductStockStatus(item).message }}
              </v-chip>
            </div>
          </template>

          <template #append>
            <div class="d-flex flex-column align-center">
              <v-number-input
                v-model="cartActions.createItemQuantityModel(item.cod_producto).value"
                control-variant="stacked"
                density="compact"
                hide-details
                :min="1"
                variant="outlined"
                width="90"
                class="mb-1"
                :error="getProductStockStatus(item).status === 'insufficient'"
              />
              
              <!-- Indicador visual de stock crítico -->
              <v-tooltip
                v-if="getProductStockStatus(item).status === 'insufficient'"
                text="Stock insuficiente"
                location="left"
              >
                <template #activator="{ props: tooltipProps }">
                  <v-icon
                    v-bind="tooltipProps"
                    size="small"
                    color="error"
                    class="mt-1"
                  >
                    mdi-alert-circle
                  </v-icon>
                </template>
              </v-tooltip>
              
              <v-tooltip
                v-else-if="getProductStockStatus(item).status === 'low'"
                text="Stock bajo"
                location="left"
              >
                <template #activator="{ props: tooltipProps }">
                  <v-icon
                    v-bind="tooltipProps"
                    size="small"
                    color="warning"
                    class="mt-1"
                  >
                    mdi-alert
                  </v-icon>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-list-item>
      </v-list>
    </template>

    <!-- Estado vacío -->
    <template v-else>
      <v-container class="text-center py-8">
        <v-icon size="64" color="grey-lighten-2" class="mb-4">
          mdi-cart-outline
        </v-icon>
        <div class="text-h6 text-grey-darken-1 mb-2">
          Carrito vacío
        </div>
        <div class="text-body-2 text-grey">
          Agrega productos para comenzar tu compra
        </div>
      </v-container>
    </template>

    <!-- Footer con totales y acciones -->
    <template #append>
      <v-divider />
      <v-container class="py-4">
        <!-- Totales -->
        <template v-if="hasItems">
          <v-card variant="tonal" color="primary" class="mb-3">
            <v-card-text class="py-3">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-body-1 font-weight-medium">Subtotal USD:</span>
                <span class="text-h6 font-weight-bold">
                  ${{ formatPrice(cartActions.getCartTotal()) }}
                </span>
              </div>
              <div class="d-flex justify-space-between align-center">
                <span class="text-body-1 font-weight-medium">Total Bs:</span>
                <span class="text-h6 font-weight-bold text-success">
                  Bs {{ totalBolivares }}
                </span>
              </div>
            </v-card-text>
          </v-card>

          <!-- Resumen de estado de stock -->
          <v-card
            v-if="currentStockValidation.hasErrors || currentStockValidation.hasWarnings"
            variant="tonal"
            :color="currentStockValidation.hasErrors ? 'error' : 'warning'"
            class="mb-3"
          >
            <!-- <v-card-text class="py-2">
              <div class="d-flex align-center">
                <v-icon 
                  :color="currentStockValidation.hasErrors ? 'error' : 'warning'"
                  size="small"
                  class="mr-2"
                >
                  {{ currentStockValidation.hasErrors ? 'mdi-alert-circle' : 'mdi-alert' }}
                </v-icon>
                <span class="text-caption">
                  {{ currentStockValidation.hasErrors ? 'Productos sin stock suficiente' : 'Productos con advertencias de stock' }}
                  ({{ currentStockValidation.errors.length + currentStockValidation.warnings.length }})
                </span>
              </div>
            </v-card-text> -->
          </v-card>

          <!-- Botones de acción -->
          <v-row dense>
            <v-col cols="6">
              <v-btn
                block
                color="error"
                variant="outlined"
                prepend-icon="mdi-delete"
                @click="cartActions.clearCart()"
              >
                Limpiar
              </v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn
                block
                color="success"
                variant="flat"
                prepend-icon="mdi-cash-register"
                :loading="submittingSale"
                :disabled="!canProceedSale"
                @click="handlerPay()"
              >
                Pagar
              </v-btn>
            </v-col>
          </v-row>

          <!-- Información adicional del carrito -->
          <!-- <div class="text-center mt-3">
            <div class="text-caption text-grey">
              {{ selectedItems.length }} {{ selectedItems.length === 1 ? 'producto' : 'productos' }} en el carrito
            </div>
            <div v-if="currentStockValidation.hasErrors || currentStockValidation.hasWarnings" class="text-caption mt-1">
              <v-icon size="x-small" class="mr-1">mdi-information</v-icon>
              Revisa el estado del stock antes de proceder
            </div>
          </div> -->
        </template>

        <!-- Botón para actualizar tasa cuando está vacío -->
        <!-- <template v-else>
          <v-btn
            block
            variant="outlined"
            prepend-icon="mdi-refresh"
            @click="fetchTasas"
            :loading="tasas === 0"
            class="mb-2"
          >
            Actualizar Tasa
          </v-btn>
          
          <v-btn
            block
            variant="outlined"
            prepend-icon="mdi-package-variant"
            @click="fetchProductosStock"
            :loading="loading"
          >
            Actualizar Stock
          </v-btn>
        </template> -->
      </v-container>
    </template>
  </v-navigation-drawer>

  <!-- Diálogo de Venta integrado -->
  <SaleForm
    v-model:show="showSaleDialog"
    :loading="submittingSale"
    title="Procesar Venta"
    :productos="selectedItems"
    :errors="saleErrors"
    :tasa_cambio="tasas"
    :clientes="clientes"
    @submit="handleSubmitSale"
    @update:show="closeSaleDialog"
  />
  
  <SaleBillModal
    v-model:show="showFactura"
    :venta="facturaVenta"
    :detalles="facturaDetalles"
    :clientes="clientes"
  />
</template>

<style scoped>
.v-list-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.v-list-item:last-child {
  border-bottom: none;
}

.v-list-item.border-error {
  border-left: 4px solid rgb(var(--v-theme-error));
  background-color: rgba(var(--v-theme-error), 0.05);
}

.v-number-input {
  max-width: 90px;
}

/* Animación para chips de stock */
.v-chip {
  transition: all 0.3s ease;
}

.v-chip:hover {
  transform: scale(1.05);
}
</style>