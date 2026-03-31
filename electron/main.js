const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let serverProcess = null;
const PORT = 3111;

function startServer() {
  const isDev = process.env.NODE_ENV === 'development';

  if (isDev) {
    // In dev mode, assume Next.js is already running on port 3000
    return Promise.resolve('http://localhost:3000');
  }

  // In production, spawn the standalone Next.js server
  const serverDir = path.join(process.resourcesPath, 'app');
  const nodeBin = process.execPath; // Electron's Node.js can run it

  return new Promise((resolve, reject) => {
    serverProcess = spawn(nodeBin, ['server.js'], {
      cwd: serverDir,
      env: {
        ...process.env,
        NODE_ENV: 'production',
        PORT: String(PORT),
        DATABASE_URL: path.join(app.getPath('userData'), 'alcloud.db'),
      },
      stdio: 'pipe',
      windowsHide: true,
    });

    serverProcess.stdout?.on('data', (data) => {
      const msg = data.toString();
      if (msg.includes('Ready') || msg.includes('started') || msg.includes('listening')) {
        resolve(`http://localhost:${PORT}`);
      }
    });

    serverProcess.stderr?.on('data', (data) => {
      const msg = data.toString();
      if (msg.includes('Ready') || msg.includes('started') || msg.includes('listening')) {
        resolve(`http://localhost:${PORT}`);
      }
    });

    // Fallback: resolve after a short delay
    setTimeout(() => resolve(`http://localhost:${PORT}`), 2000);

    serverProcess.on('error', reject);
  });
}

async function createWindow() {
  const url = await startServer();

  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    title: 'aLCloud',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    backgroundColor: '#0f172a',
    show: false,
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.loadURL(url);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (serverProcess) {
    serverProcess.kill();
    serverProcess = null;
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (serverProcess) {
    serverProcess.kill();
    serverProcess = null;
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
