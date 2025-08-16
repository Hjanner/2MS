import { app, BrowserWindow } from 'electron'
import { join, dirname } from 'path'
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { existsSync } from 'fs'

// Crear __dirname para ES modules
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

let mainWindow
let pythonProcess

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    show: true,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // Abrir DevTools en desarrollo
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
  } else {
    // Cargar desde el sistema de archivos
    const indexPath = join(__dirname, '../dist/index.html');
    console.log('Loading file:', indexPath);
    mainWindow.loadFile(indexPath);
  }

  // Log de eventos para debug
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('Failed to load:', errorCode, errorDescription);
  });

  mainWindow.webContents.on('did-finish-load', () => {
    console.log('Page loaded successfully');
  });
}

app.whenReady().then(() => {
  initializeApp()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    stopBackend()
    app.quit()
  }
})

async function initializeApp() {
  console.log('Initializing app...')
  
  try {
    await startBackend()
    console.log('Backend started successfully')
    
    // Esperar que el backend esté listo
    await waitForBackend()
    
    createWindow()
    console.log('Window created')
  } catch (error) {
    console.error('Error initializing app:', error)
    // Crear ventana aunque haya errores
    createWindow()
  }
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const isDev = process.env.NODE_ENV === 'development'
    
    // Rutas según el entorno
    let pythonPath, backendDir, mainPyPath
    
    if (isDev) {
      pythonPath = join(__dirname, '../backend/venv/Scripts/python.exe')
      backendDir = join(__dirname, '../backend')
      mainPyPath = join(backendDir, 'main.py')
    } else {
      // En producción, el backend está en resources
      pythonPath = join(process.resourcesPath, 'backend/venv/Scripts/python.exe')
      backendDir = join(process.resourcesPath, 'backend')
      mainPyPath = join(backendDir, 'main.py')
      
      // Fallback si no encuentra el venv empaquetado
      if (!existsSync(pythonPath)) {
        // Usar Python del sistema
        pythonPath = 'python'
      }
    }
    
    console.log('Python path:', pythonPath)
    console.log('Backend dir:', backendDir)
    console.log('Main.py path:', mainPyPath)
    console.log('Python exists:', existsSync(pythonPath))
    console.log('Backend dir exists:', existsSync(backendDir))
    console.log('Main.py exists:', existsSync(mainPyPath))
    
    // Configurar variables de entorno para el backend
    const env = {
      ...process.env,
      SQLITE_DB: join(backendDir, '2MS.db'),
      PORT: '8000',
      HOST: '127.0.0.1'
    }
    
    pythonProcess = spawn(pythonPath, ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000', '--log-level', 'info'], {
      cwd: backendDir,
      env: env
    })

    pythonProcess.stdout.on('data', (data) => {
      const output = data.toString()
      console.log(`Backend: ${output}`)
      if (output.includes('Uvicorn running') || output.includes('Application startup complete')) {
        resolve()
      }
    })

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Backend Error: ${data}`)
    })

    pythonProcess.on('error', (error) => {
      console.error('Failed to start backend:', error)
      reject(error)
    })

    pythonProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`)
    })

    // Timeout si no se inicia en 10 segundos
    setTimeout(() => {
      console.log('Backend startup timeout - continuing anyway')
      resolve()
    }, 10000)
  })
}

async function waitForBackend() {
  const maxAttempts = 30
  let attempts = 0
  
  while (attempts < maxAttempts) {
    try {
      const response = await fetch('http://127.0.0.1:8000/health')
      if (response.ok) {
        console.log('Backend is ready!')
        return
      }
    } catch (error) {
      // Backend no está listo aún
    }
    
    attempts++
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
  
  console.warn('Backend may not be ready, but continuing...')
}

function stopBackend() {
  if (pythonProcess) {
    pythonProcess.kill()
    pythonProcess = null
  }
}