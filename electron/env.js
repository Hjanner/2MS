export function getEnvironmentConfig() {
  const isDevelopment = process.env.NODE_ENV === 'development'
  
  return {
    API_URL: isDevelopment 
      ? 'http://localhost:8000' 
      : 'http://127.0.0.1:8000',
    
    BASE_URL: isDevelopment 
      ? 'http://localhost:3000' 
      : 'file://',
      
    SQLITE_DB: isDevelopment 
      ? '2MS.db' 
      : '2MS.db'
  }
}