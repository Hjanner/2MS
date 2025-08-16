# 2MS
Morela's Management System (2MS) está diseñado para automatizar y optimizar los procesos clave del Cafetin Morela. 
Este proyecto utiliza FastAPI como backend y Vue 3 + Electron como frontend para crear una aplicación interactiva de escritorio y web.

# Requisitos
Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- Python 3.9 o superior
- pip (administrador de paquetes de Python)
- Node.js y npm

# Instalación
Clona este repositorio:

```bash
git clone https://github.com/Hjanner/2MS.git
cd 2MS
```

Activa un entorno virtual (opcional pero recomendado):  
En Windows:
```bash
venv\Scripts\activate
```
En Linux:
```bash
source venv/bin/activate
```

Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

Instala las dependencias de Node.js:

```bash
npm install
```

# Crear y llenar base de datos, con datos beta

```bash
python database/create_db.py
python database/insert_db.py
python database/triggers_db.py
python database/views_db.py   
```

O puedes ejecutar todos los scripts de la base de datos con:

```bash
npm run db:init
```

# Comandos para desarrollo

## Primera terminal (Backend + DB):

```bash
cd backend
../venv/Scripts/activate  # O venv\Scripts\activate si estás en la raíz
uvicorn main:app --reload
```

Ejecuta los scripts de la base de datos si es necesario:

```bash
npm run db:init
```

## Segunda terminal (Frontend Vue + Electron):

```bash
npm run electron:dev
```

Esto iniciará el frontend en modo desarrollo y abrirá la aplicación de escritorio con Electron.

---

# Ejecución en producción
Compila el frontend y ejecuta la app de escritorio:

## 1. Construir frontend
```bash
npm run build
```

## 2. Ejecutar scripts de base de datos (opcional, dependiendo de tu flujo)
```bash
npm run db:init
```

## 3. Construir aplicación Electron
```bash
npm run electron:build
```

```bash
npm run build
npm run electron:build
```

---

# Acceso a la aplicación web

- Frontend Vue: http://localhost:3000 (en desarrollo)
- Documentación interactiva FastAPI: http://127.0.0.1:8000/docs

---

# Script para guardar tasa del BCV

```bash
python -m backend.utilities.save_tasa
```

Usar **Task Scheduler de Windows**
#### 1. **Configura el Task Scheduler de Windows**

1. **Abre el Programador de tareas** (Task Scheduler).
2. **Crea una nueva tarea básica**:
   - Nombre: `GuardarTasaDolar`
   - Descripción: Guarda la tasa de cambio automáticamente a las 4:00 PM.
3. **Programa la tarea**:
   - Elige “Diariamente” o según prefieras.
   - Hora de inicio: **16:00** (4:00 PM).
   - Asegúrate de que la hora de tu sistema esté en la zona horaria de Venezuela (UTC-4).
4. **Acción**:  
   - Elige “Iniciar un programa”.
   - Programa/script:  
     - Ruta a tu ejecutable de Python, por ejemplo:  
       `D:\desarrollo\2MS\2MS\backend\utilities\save_tasa.exe`
   - Agrega argumentos:  
     - Ruta absoluta a tu script, por ejemplo:  
       `D:\desarrollo\2MS\2MS\backend\utilities\save_tasa.py`
   - (Opcional) Establece el directorio de inicio en la carpeta de tu proyecto.
5. **Guarda la tarea**.

---

#### 2. **Verifica la ejecución**

- Puedes probar ejecutando el script manualmente:
  ```bash
  python -m backend.utilities.save_tasa
  ```
- Revisa que la tasa se guarde correctamente en la base de datos.

# Licencia
Este proyecto está bajo la licencia