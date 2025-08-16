import { app, BrowserWindow } from 'electron'
import { join, dirname } from 'path'
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { runDatabaseScripts } from './database.js'

// Crear __dirname para ES modules
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

let mainWindow
let pythonProcess

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    show: true, // Forzar que se muestre
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // SIEMPRE abrir DevTools para debug
  mainWindow.webContents.openDevTools();

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
  // Temporalmente: solo crear la ventana sin backend
  createWindow();
  console.log('App ready, window created');

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
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    await runDatabaseScripts()
    console.log('Database scripts completed')
    
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
    // Ajustar rutas según el entorno
    const pythonPath = process.env.NODE_ENV === 'development'
      ? join(__dirname, '../backend/venv/Scripts/python.exe')
      : join(process.resourcesPath, 'backend/venv/Scripts/python.exe')
    
    const backendDir = process.env.NODE_ENV === 'development'
      ? join(__dirname, '../backend')
      : join(process.resourcesPath, 'backend')
    
    // Verificar si el archivo Python existe
    console.log('Python path:', pythonPath)
    console.log('Backend dir:', backendDir)
    console.log('NODE_ENV:', process.env.NODE_ENV)
    
    pythonProcess = spawn(pythonPath, ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'], {
      cwd: backendDir,
      env: { ...process.env }
    })

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python: ${data}`)
      if (data.toString().includes('Uvicorn running')) {
        resolve()
      }
    })

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`)
    })

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error)
      reject(error)
    })

    // Timeout en caso de que no se inicie correctamente
    setTimeout(() => {
      resolve() // Continuar aunque no hayamos recibido confirmación
    }, 5000)
  })
}

function stopBackend() {
  if (pythonProcess) {
    pythonProcess.kill()
    pythonProcess = null
  }
}