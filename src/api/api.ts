import axios from "axios";

const api = axios.create({
    baseURL:  process.env.API_URL || 'http://localhost:8000',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.response.use(
    response => response,
    error => {
      console.error('API Error:', error);
      return Promise.reject(error);
    }
);
  
export default api;