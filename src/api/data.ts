export const DEPARTAMENTOS: string[] = [
    'CIAP',
    'CADH',
    'CHSL',
    'CIEPV',
    'Centro de Estudios Regionales',
    'Consultoría Jurídica',
    'Coordinación Administración de Personal',
    'Coordinación General de Recursos Humanos',
    'Coordinación General de Servicios Financieros',
    'Coordinación General de Tecnología de la Información',
    'Coordinación de Administración Académica',
    'Coordinación de Archivo',
    'Coordinación de Auditoria Interna',
    'Coordinación de Biblioteca',
    'Coordinación de Comisión Disciplinaria',
    'Coordinación de Compras y Almacenes',
    'Coordinación de Comunicaciones',
    'Coordinación de Cooperación Económica',
    'Coordinación de Cultura',
    'Coordinación de Deportes',
    'Coordinación de Desarrollo del Talento',
    'Coordinación de Egresados',
    'Coordinación de Gestión Estudiantil',
    'Coordinación de Idiomas',
    'Coordinación de Innovación y Emprendimiento',
    'Coordinación de Internacionalización',
    'Coordinación de Materias Comunes de Ingeniería',
    'Coordinación de Mercadeo Institucional',
    'Coordinación de Promoción',
    'Coordinación de Relaciones Institucionales',
    'Coordinación de Relaciones Interinstitucionales',
    'Coordinación de Relaciones Internacionales',
    'Coordinación de Seguridad',
    'Coordinación de Seguridad y Salud Laboral',
    'Coordinación de Servicios Financieros',
    'Coordinación de Sustentabilidad Ambiental',
    'Coordinación de la Comisión Disciplinaria',
    'Crédito y Cobranzas',
    'Decanato de Ingenieria',
    'Dir. Gen. de Identidad, Desarrollo Estudiantil y Extensión Social',
    'Direccion de Planificacion y Gestión Estrategica',
    'Direccion de Proyectos Especiales',
    'Dirección General Académica',
    'Dirección General de Finanzas y Administración',
    'Dirección de Calidad y Mejora Continua',
    'Dirección de Comunicación, Mercadeo y Promoción',
    'Dirección de Desarrollo Estudiantil',
    'Dirección de Extensión Social Universitaria',
    'Dirección de Identidad y Misión',
    'Dirección de Postgrado',
    'Dirección de Secretaría',
    'Dirección de Servicios Generales',
    'Escuela de Administración y Contaduría',
    'Escuela de Ciencias Sociales',
    'Escuela de Comunicación Social',
    'Escuela de Derecho',
    'Escuela de Educación',
    'Escuela de Ingeniería Civil',
    'Escuela de Ingeniería Industrial',
    'Escuela de Ingeniería en Informática',
    'Facultad de Ingeniería',
    'Oficina de Derechos Humanos',
    'Plan Estratégico (Ejes)',
    'Unidad de Innovación y Desarrollo Académico',
    'Vicerrectorado',
    'Seguros Mercantil',
];

export const UNIDADES_MEDIDAS = [
  'unidad',
  'kg',
  'gramos',
  'litros',
  'mililitros',
  'piezas',
  'metros',
  'centímetros'
];

export const TIPO_MOVIMIENTO_OPTIONS = [
  {
    title: 'Entrada (Aumentar stock)',
    value: 'entrada',
    icon: 'mdi-arrow-up-bold',
    color: 'success'
  },
  {
    title: 'Salida (Reducir stock)',
    value: 'salida',
    icon: 'mdi-arrow-down-bold',
    color: 'error'
  }
];

// Opciones para la referencia de movimientos de salida
export const REFERENCIA_OPTIONS = [
  {
    title: 'Descarte',
    value: 'descarte',
    icon: 'mdi-delete',
    color: 'error'
  },
  {
    title: 'Ajuste',
    value: 'ajuste',
    icon: 'mdi-tune',
    color: 'warning'
  },
  {
    title: 'Traslado a tienda',
    value: 'traslado_tienda',
    icon: 'mdi-store',
    color: 'info'
  },
  {
    title: 'Autoconsumo',
    value: 'autoconsumo',
    icon: 'mdi-food-fork-drink',
    color: 'purple'
  }
];

// Opciones para el tipo de categoría
export const TIPO_OPTIONS = [
  { 
    value: 'preparado', 
    title: 'Preparado',
    subtitle: 'Productos que requieren preparación',
    icon: 'mdi-chef-hat',
    color: 'success'
  },
  { 
    value: 'noPreparado', 
    title: 'No Preparado',
    subtitle: 'Productos listos para consumo',
    icon: 'mdi-package-variant',
    color: 'warning'
  }
];

export const TIPOS_VENTA = [
  { title: 'De Contado', value: 'de_contado' },
  { title: 'Crédito', value: 'credito' }
]

export const METODOS_PAGO = [
  { title: 'Efectivo Bs', value: 'efectivo_bs' },
  { title: 'Efectivo USD', value: 'efectivo_usd' },
  { title: 'Pago Móvil', value: 'pago_movil' },
  { title: 'Débito', value: 'debito' },
  { title: 'Transferencia', value: 'transferencia' }
]