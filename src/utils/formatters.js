export function formatCurrency(amount) {
    return new Intl.NumberFormat('es-VE', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(amount);
}

export function formatCurrencyBs(amount) {
    return new Intl.NumberFormat('es-VE', {
      style: 'currency',
      currency: 'VES',
      minimumFractionDigits: 2
    }).format(amount);
}
  
export function getStockColor(producto) {
    if (producto.tipo_producto === 'preparado') return 'grey';
    if (producto.cant_actual <= 0) return 'red';
    if (producto.cant_actual <= producto.cant_min) return 'orange';
    return 'green';
}
  
export function getStockStatus(producto) {
    if (producto.tipo_producto === 'preparado') return 'N/A';
    if (producto.cant_actual <= 0) return 'Sin stock';
    if (producto.cant_actual <= producto.cant_min) return 'Stock bajo';
    return 'Disponible';
}

export function getCurrentDate() {
    return new Date().toISOString().split('T')[0];
}

export function getCurrentTimeStamp () {
    return Date.now();
}