const { spawn } = require('child_process')
const path = require('path')

function runDatabaseScripts() {
  return new Promise((resolve) => {
    const scripts = [
      'create_db.py',
      'insert_db.py',
      'triggers_db.py',
      'views_db.py'
    ]
    
    const pythonPath = process.env.NODE_ENV === 'development'
      ? path.join(__dirname, '../backend/venv/Scripts/python.exe')
      : path.join(process.resourcesPath, 'backend/venv/Scripts/python.exe')
    
    let completed = 0
    
    scripts.forEach(script => {
      const scriptPath = process.env.NODE_ENV === 'development'
        ? path.join(__dirname, `../database/${script}`)
        : path.join(process.resourcesPath, `database/${script}`)
      
      const process = spawn(pythonPath, [scriptPath], {
        cwd: process.env.NODE_ENV === 'development'
          ? path.join(__dirname, '../database')
          : path.join(process.resourcesPath, 'database')
      })
      
      process.stdout.on('data', (data) => {
        console.log(`DB ${script}: ${data}`)
      })
      
      process.stderr.on('data', (data) => {
        console.error(`DB ${script} ERROR: ${data}`)
      })
      
      process.on('close', () => {
        completed++
        if (completed === scripts.length) resolve()
      })
    })
  })
}

module.exports = { runDatabaseScripts }