import { ref, computed, readonly } from 'vue'
import api from '@/api/api'
import { useSnackbar } from '@/composables/useSnackbar'

const productosStock = ref([])
const loading = ref(false)

export function useStockValidation() {
  const { showSnackbar } = useSnackbar()

  // Función para mostrar notificaciones de stock
  function showStockNotifications(validation) {
    // Mostrar errores críticos
    if (validation.hasErrors) {
      validation.errors.forEach(error => {
        showSnackbar(error.mensaje, 'error')
      })
    }
    
    // Mostrar advertencias
    if (validation.hasWarnings) {
      validation.warnings.forEach(warning => {
        if (warning.tipo !== 'unknown_stock') { // No mostrar advertencias para productos preparados
          showSnackbar(warning.mensaje, 'warning')
        }
      })
    }
  }

  // Función para verificar si se puede proceder con la venta
  function canProceedWithSale(cartItems) {
    const validation = validateCartStock(cartItems)
    showStockNotifications(validation)
    return !validation.hasErrors
  }

  // Función para obtener un resumen del estado de stock del carrito
  function getCartStockSummary(cartItems) {
    const validation = validateCartStock(cartItems)
    
    return {
      ...validation,
      totalProducts: cartItems.length,
      productsWithIssues: validation.errors.length + validation.warnings.length,
      canProceed: !validation.hasErrors
    }
  }

  return {
    // Estados reactivos
    productosStock: readonly(productosStock),
    loading: readonly(loading),
    
    // Computed properties
    lowStockProducts,
    outOfStockProducts,
    criticalStockProducts,
    
    // Funciones
    fetchProductosStock,
    validateCartStock,
    getProductStockStatus,
    showStockNotifications,
    canProceedWithSale,
    getCartStockSummary
  }
} 
//Computed para productos con diferentes estados de stock
  const lowStockProducts = computed(() => {
    return productosStock.value.filter(producto => 
      producto.cant_actual <= producto.cant_min && producto.cant_actual > 0
    )
  })

  const outOfStockProducts = computed(() => {
    return productosStock.value.filter(producto => producto.cant_actual <= 0)
  })

  const criticalStockProducts = computed(() => {
    return [...lowStockProducts.value, ...outOfStockProducts.value]
  })

  // Función para obtener información de stock
  async function fetchProductosStock() {
    loading.value = true
    try {
      const response = await api.get('/productos_noPreparados/')
      productosStock.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al cargar stock de productos:', error)
      showSnackbar('Error al cargar información de stock', 'error')
      return []
    } finally {
      loading.value = false
    }
  }

  // Función para validar stock de productos en el carrito
  function validateCartStock(cartItems) {
    const errors = []
    const warnings = []
    
    cartItems.forEach(item => {
      const stockInfo = productosStock.value.find(p => 
        p.cod_producto_noPreparado === item.cod_producto
      )
      
      if (stockInfo) {
        // Verificar si hay suficiente stock
        if (stockInfo.cant_actual < item.quantity) {
          errors.push({
            cod_producto: item.cod_producto,
            producto: item.nombre,
            cantidadSolicitada: item.quantity,
            cantidadDisponible: stockInfo.cant_actual,
            mensaje: `${item.nombre}: Stock insuficiente. Disponible: ${stockInfo.cant_actual}, Solicitado: ${item.quantity}`,
            tipo: 'insufficient_stock'
          })
        }
        // Verificar si después de la venta quedará en stock bajo
        else if ((stockInfo.cant_actual - item.quantity) <= stockInfo.cant_min) {
          warnings.push({
            cod_producto: item.cod_producto,
            producto: item.nombre,
            cantidadRestante: stockInfo.cant_actual - item.quantity,
            cantidadMinima: stockInfo.cant_min,
            mensaje: `${item.nombre}: Después de la venta quedará en stock bajo (${stockInfo.cant_actual - item.quantity}/${stockInfo.cant_min})`,
            tipo: 'will_be_low_stock'
          })
        }
      } else {
        // Producto no encontrado en inventario (podría ser preparado)
        warnings.push({
          cod_producto: item.cod_producto,
          producto: item.nombre,
          mensaje: `${item.nombre}: No se pudo verificar el stock (producto preparado)`,
          tipo: 'unknown_stock'
        })
      }
    })
    
    return { errors, warnings, hasErrors: errors.length > 0, hasWarnings: warnings.length > 0 }
  }

  // Función para obtener el estado del stock de un producto específico
  function getProductStockStatus(item) {
    const stockInfo = productosStock.value.find(p => 
      p.cod_producto_noPreparado === item.cod_producto
    )
    
    if (!stockInfo) {
      return { 
        status: 'unknown', 
        message: 'Stock no disponible',
        color: 'grey',
        icon: 'mdi-help-circle'
      }
    }
    
    if (stockInfo.cant_actual < item.quantity) {
      return { 
        status: 'insufficient', 
        message: `Stock insuficiente (${stockInfo.cant_actual} disponibles)`,
        color: 'error',
        icon: 'mdi-alert-circle'
      }
    }
    
    if (stockInfo.cant_actual <= stockInfo.cant_min) {
      return { 
        status: 'low', 
        message: `Stock bajo (${stockInfo.cant_actual}/${stockInfo.cant_min})`,
        color: 'warning',
        icon: 'mdi-alert'
      }
    }
    
    if ((stockInfo.cant_actual - item.quantity) <= stockInfo.cant_min) {
      return { 
        status: 'will_be_low', 
        message: `Quedará en stock bajo (${stockInfo.cant_actual - item.quantity}/${stockInfo.cant_min})`,
        color: 'orange',
        icon: 'mdi-alert-outline'
      }
    }
    
    return { 
      status: 'ok', 
      message: `Stock disponible (${stockInfo.cant_actual})`,
      color: 'success',
      icon: 'mdi-check'
    }
}

  //