const { app, BrowserWindow } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let mainWindow
let pythonProcess

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    // Cargar desde el sistema de archivos
    mainWindow.loadFile(path.join(__dirname, '../../dist/index.html'));
  }
}

app.whenReady().then(() => {
  // Iniciar el backend de Flask
//   startBackend()
  
//   const { runDatabaseScripts } = require('./database')
//   runDatabaseScripts()


//   createWindow()  initializeApp()

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
  await startBackend()
  
  // Esperar que el backend esté listo
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  await runDatabaseScripts()
  createWindow()
}

function startBackend() {
  // Ajusta estas rutas según tu proyecto
  const pythonPath = path.join(__dirname, '../backend/venv/Scripts/python.exe')
  const scriptPath = path.join(__dirname, '../backend/main.py')
  
  pythonProcess = spawn(pythonPath, ['-m', 'uvicorn', 'main:app'], {
    cwd: path.join(__dirname, '../backend')
  })

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python: ${data}`)
  })

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`)
  })
}

function stopBackend() {
  if (pythonProcess) {
    pythonProcess.kill()
    pythonProcess = null
  }
}