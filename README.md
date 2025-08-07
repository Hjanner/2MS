# 2MS
Morela's Management System (2MS) está diseñado para automatizar y optimizar los procesos clave del Cafetin Morela. 
Este proyecto utiliza FastAPI como backend y ReactPy como frontend para crear una aplicación interactiva.

# Requisitos
Antes de comenzar, asegúrate de tener instalados los siguientes programas:

Python 3.9 o superior
pip (administrador de paquetes de Python)

# Instalación
Clona este repositorio:

git clone https://github.com/Hjanner/2MS.git
cd 2MS
Activa un entorno virtual (opcional pero recomendado): En Windows: bash venv\Scripts\activate  En Linux: bash source venv/bin/activate 

Instala las dependencias:

pip install -r requirements.txt

# crear y llenar base de datos, con datos beta
```bash
python database/create_db.py
```

```bash
python database/insert_db.py
```

```bash
python database/triggers_db.py
```

# Ejecución
Inicia el servidor FastAPI:

uvicorn backend.main:app --reload
Accede a la aplicación en tu navegador:

Frontend ReactPy: http://127.0.0.1:8000
Documentación interactiva: http://127.0.0.1:8000/docs

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
Este proyecto está bajo la licencia MIT.

