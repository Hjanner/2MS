export const validateRequired = (fieldName = 'Este campo') => 
  (value) => !!value || `${fieldName} es requerido`;

export const validateCode = (value) => {
  if (!value) return 'Código es requerido';
  if (value.length < 3) return 'Código debe tener al menos 3 caracteres';
  if (value.length > 20) return 'Código debe tener máximo 20 caracteres';
  return true;
};

export const validatePrice = (value) => {
  if (!value) return 'Precio es requerido';
  const num = parseFloat(value);
  if (isNaN(num)) return 'Precio debe ser un número válido';
  if (num <= 0) return 'Precio debe ser mayor a 0';
  return true;
};

export const validatePositiveNumber = (fieldName = 'Este campo') => 
  (value) => {
    if (!value) return `${fieldName} es requerido`;
    const num = parseFloat(value);
    if (isNaN(num)) return `${fieldName} debe ser un número válido`;
    if (num < 0) return `${fieldName} debe ser mayor o igual a 0`;
    return true;
  };

export const validateMinQuantity = validatePositiveNumber('Cantidad mínima');

export const validateCost = (value) => {
  if (!value) return 'Costo de compra es requerido';
  const num = parseFloat(value);
  if (isNaN(num)) return 'Costo debe ser un número válido';
  if (num <= 0) return 'Costo debe ser mayor a 0';
  return true;
};

export const validatePhone = (value) => {
  if (!value) return 'Teléfono es requerido';
  if (!/^\d+$/.test(value)) return 'Teléfono debe ser un número';
  if (value.length !== 11) return 'Teléfono debe tener 11 dígitos';
  return true;
};

export const validateImage = (value) => {
  if (!value) return 'Imagen es requerida';
  if (value.size > 2 * 1024 * 1024) return 'La imagen no debe exceder 2MB';
  if (!['image/jpeg', 'image/png', 'image/gif'].includes(value.type)) {
    return 'Formato no soportado (use JPG, PNG o GIF)';
  }
  return true;
};

export const validateRIF = (value) => {
  if (!value) return true; // Opcional
  if (!/^[JGVEP]\d{9}\d$/.test(value)) {
    return 'Formato de RIF inválido (ej: J12345678)';
  }
  return true;
};

// Validación para emails
export const validateEmail = (value) => {
  if (!value) return true; // Opcional
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(value) || 'Email inválido';
};

// Validación para porcentajes (0-100)
export const validatePercentage = (value) => {
  if (!value) return 'Porcentaje es requerido';
  const num = parseFloat(value);
  if (isNaN(num)) return 'Debe ser un número válido';
  if (num < 0 || num > 100) return 'Debe estar entre 0 y 100';
  return true;
};

// Validación para fechas futuras
export const validateFutureDate = (value) => {
  if (!value) return 'Fecha es requerida';
  const date = new Date(value);
  const today = new Date();
  return date > today || 'La fecha debe ser futura';
};
// Validación para cédula de identidad
export const validateCI = (value) => {
  if (!value) return 'Cédula es requerida';
  if (!/^\d+$/.test(value)) return 'Cédula debe ser un número';
  if (value.length < 6) return 'Cédula muy corta (mín 6 dígitos)';
  if (value.length > 9) return 'Cédula muy larga (máx 9 dígitos)';
  return true;
};

// Validación para departamentos
export const validateDepartment = (value) => {
  if (!value) return 'Departamento es requerido';
  return true;
};