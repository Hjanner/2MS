const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  // Aquí puedes exponer APIs seguras para el renderer
})