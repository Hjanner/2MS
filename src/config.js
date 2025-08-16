// Detectar si estamos en Electron
const isElectron = window.navigator.userAgent.toLowerCase().indexOf('electron') > -1

// Configuración de la API
export const API_CONFIG = {
  baseURL: isElectron 
    ? 'http://127.0.0.1:8000'  // En Electron
    : import.meta.env.VITE_API_URL || 'http://localhost:8000', // En desarrollo web
    
  timeout: 10000,
  
  headers: {
    'Content-Type': 'application/json'
  }
}

export const isElectronApp = isElectron

console.log('API Config:', API_CONFIG)
console.log('Is Electron:', isElectron)