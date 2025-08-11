<script setup>
import { inject, toRefs, ref } from 'vue'
import SaleForm from '@/components/sale/SaleForm.vue'
import { useSnackbar } from '@/composables/useSnackbar'
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

// Estados para el diálogo de venta
const showSaleDialog = ref(false)
const submittingSale = ref(false)
const saleErrors = ref({})
const tasas = ref(0)

// Función para obtener tasas de cambio
async function fetchTasas() {
  try {
    const response = await api.get('/dolar')
    tasas.value = response.data.valor_usd_bs
    console.log('Tasa obtenida:', tasas.value);
  } catch (error) {
    console.error('Error al cargar tasas:', error)
    showSnackbar('Error al cargar las tasas de cambio', 'error')
    // Valor por defecto si falla
    tasas.value = 36.50
  }
}

// Función para manejar el pago
async function handlerPay() {
  if (selectedItems.value.length === 0) {
    showSnackbar('No hay productos en el carrito', 'warning')
    return
  }
  
  // Cargar tasas antes de abrir el diálogo
  await fetchTasas()
  showSaleDialog.value = true
}

// Función para manejar el envío de la venta
async function handleSubmitSale(ventaCompleta) {
  submittingSale.value = true
  saleErrors.value = {}
  
  try {
    console.log('Datos completos a enviar:', ventaCompleta);
    
    // Usar el nuevo endpoint transaccional que maneja todo en una sola operación
    const response = await api.post('/ventas/registrar', {
      venta: ventaCompleta.venta,
      detalles: ventaCompleta.detalles,
      pago: ventaCompleta.pago
    })
    
    console.log('Venta registrada con ID:', response.data.id_venta);
    
    showSnackbar('Venta registrada correctamente', 'success')
    showSaleDialog.value = false
    cartActions.clearCart() // Limpiar el carrito después de la venta exitosa
    
  } catch (error) {
    console.error('Error al registrar la venta:', error)
    
    // Manejar errores específicos de la transacción
    if (error.response?.data?.detail) {
      showSnackbar(error.response.data.detail, 'error')
    } else {
      showSnackbar('Error al registrar la venta', 'error')      // Error genérico
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
      const errorMessages = Object.values(backendErrors).join(', ')
      showSnackbar(errorMessages || 'Ocurrió un error inesperado.', 'error')
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

function closeSaleDialog() {
  showSaleDialog.value = false
  saleErrors.value = {}
}
</script>

<template>
  <v-navigation-drawer
    location="right"
    :width="500"
  >
    <v-list nav>
      <v-list-item
        v-for="(item, key) in selectedItems"
        :key="item.cod_producto"
        :class="key % 2 === 0 ? 'bg-grey-lighten-3' : ''"
        density="compact"
        lines="two"
      >
        <template #subtitle>
          <span class="text-subtitle-2">
            USD {{ cartActions.getItemTotal(item.cod_producto).toFixed(2) }}
          </span>
        </template>

        <template #title>
          <span class="text-subtitle-2">
            {{ item.nombre }}
          </span>
        </template>

        <template #prepend>
          <v-icon
            class="cursor-pointer"
            icon="mdi-delete-outline"
            @click="cartActions.removeItem(item.cod_producto)"
          />
        </template>

        <template #append>
          <v-number-input
            v-model="cartActions.createItemQuantityModel(item.cod_producto).value"
            control-variant="stacked"
            density="compact"
            hide-details
            :min="1"
            variant="outlined"
            width="80"
          />
        </template>
      </v-list-item>
    </v-list>

    <template #append>
      <v-container>
        <v-row class="mb-2 d-flex justify-space-between" dense>
          <span class="text-h6">
            Total
          </span>

          <span class="text-h6">
            USD {{ cartActions.getCartTotal().toFixed(2) }}
          </span>
        </v-row>

        <v-row dense>
          <v-col>
            <v-btn
              block
              color="primary"
              text="eliminar"
              variant="outlined"
              @click="cartActions.clearCart()"
            />
          </v-col>

          <v-col>
            <v-btn
              block
              color="primary"
              text="pagar"
              variant="flat"
              @click="handlerPay()"
            />
          </v-col>
        </v-row>
      </v-container>
    </template>
  </v-navigation-drawer>

  <!-- Diálogo de Venta -->
  <SaleForm
    v-model:show="showSaleDialog"
    :loading="submittingSale"
    title="Procesar Venta"
    :productos="selectedItems"
    :errors="saleErrors"
    :tasa_cambio="tasas"
    @submit="handleSubmitSale"
    @update:show="closeSaleDialog"
  />
</template>