import axios from "axios";

// Detectar si estamos en Electron
const isElectron = () => {
    return window.navigator.userAgent.toLowerCase().indexOf('electron') > -1;
};

// Detectar si estamos en desarrollo
const isDevelopment = () => {
    return import.meta.env.DEV || import.meta.env.MODE === 'development';
};

// Configurar la URL base según el entorno
const getBaseURL = () => {
    if (isElectron()) {
        // En Electron (producción), conectar directamente al backend
        return 'http://127.0.0.1:8000';
    } else if (isDevelopment()) {
        // En desarrollo web, usar el proxy
        return '/api';
    } else {
        // En producción web (si es que la tienes)
        return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    }
};

const baseURL = getBaseURL();

console.log('API Configuration:', {
    isElectron: isElectron(),
    isDevelopment: isDevelopment(),
    baseURL: baseURL,
    userAgent: window.navigator.userAgent
});

const api = axios.create({
    baseURL: baseURL,
    timeout: 10000, // Aumentar timeout para Electron
    headers: {
        'Content-Type': 'application/json'
    }
});

// Interceptor de request para debugging
api.interceptors.request.use(
    config => {
        console.log('API Request:', {
            method: config.method?.toUpperCase(),
            url: config.url,
            fullURL: `${config.baseURL}${config.url}`,
            data: config.data
        });
        return config;
    },
    error => {
        console.error('Request Error:', error);
        return Promise.reject(error);
    }
);

// Interceptor de response
api.interceptors.response.use(
    response => {
        console.log('API Response:', {
            status: response.status,
            url: response.config.url,
            data: response.data
        });
        return response;
    },
    error => {
        console.error('API Error:', {
            status: error.response?.status,
            statusText: error.response?.statusText,
            data: error.response?.data,
            message: error.message,
            url: error.config?.url,
            fullURL: error.config ? `${error.config.baseURL}${error.config.url}` : 'unknown'
        });
        
        // Si es un error de conexión en Electron, mostrar mensaje más específico
        if (isElectron() && error.code === 'ECONNREFUSED') {
            console.error('Backend connection failed. Make sure the FastAPI server is running on port 8000.');
        }
        
        return Promise.reject(error);
    }
);

export default api;