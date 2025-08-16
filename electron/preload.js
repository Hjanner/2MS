import { contextBridge } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  // Aquí puedes exponer APIs seguras para el renderer
  // Ejemplo:
  // openFile: () => ipcRenderer.invoke('dialog:openFile'),
  // saveFile: (data) => ipcRenderer.invoke('dialog:saveFile', data),
})