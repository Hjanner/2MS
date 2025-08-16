import { spawn } from 'child_process'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

// Crear __dirname para ES modules
const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export function runDatabaseScripts() {
  return new Promise((resolve, reject) => {
    const scripts = [
      'create_db.py',
      'insert_db.py',
      'triggers_db.py',
      'views_db.py'
    ]
    
    const pythonPath = process.env.NODE_ENV === 'development'
      ? join(__dirname, '../backend/venv/Scripts/python.exe')
      : join(process.resourcesPath, 'backend/venv/Scripts/python.exe')
    
    let completed = 0
    let hasError = false
    
    scripts.forEach(script => {
      const scriptPath = process.env.NODE_ENV === 'development'
        ? join(__dirname, `../database/${script}`)
        : join(process.resourcesPath, `database/${script}`)
      
      const pythonProcess = spawn(pythonPath, [scriptPath], {
        cwd: process.env.NODE_ENV === 'development'
          ? join(__dirname, '../database')
          : join(process.resourcesPath, 'database')
      })
      
      pythonProcess.stdout.on('data', (data) => {
        console.log(`DB ${script}: ${data}`)
      })
      
      pythonProcess.stderr.on('data', (data) => {
        console.error(`DB ${script} ERROR: ${data}`)
      })
      
      pythonProcess.on('close', (code) => {
        completed++
        if (code !== 0) {
          hasError = true
          console.error(`Script ${script} failed with code ${code}`)
        }
        
        if (completed === scripts.length) {
          if (hasError) {
            reject(new Error('Some database scripts failed'))
          } else {
            resolve()
          }
        }
      })

      pythonProcess.on('error', (error) => {
        console.error(`Failed to run ${script}:`, error)
        hasError = true
        completed++
        if (completed === scripts.length) {
          reject(error)
        }
      })
    })
  })
}

export default { runDatabaseScripts }