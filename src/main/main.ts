/* eslint global-require: off, no-console: off, promise/always-return: off */

/**
 * This module executes inside of electron's main process. You can start
 * electron renderer process from here and communicate with the other processes
 * through IPC.
 *
 * When running `npm run build` or `npm run build:main`, this file is compiled to
 * `./src/main.js` using webpack. This gives us some performance wins.
 */
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import path from 'path';
import { app, BrowserWindow, shell, ipcMain, dialog } from 'electron';
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';
import { ChildProcess, execFile } from 'child_process';
import { existsSync } from 'fs';
import { stdout } from 'process';
import MenuBuilder from './menu';
import { resolveHtmlPath } from './util';

export default class AppUpdater {
    constructor() {
        log.transports.file.level = 'info';
        autoUpdater.logger = log;
        autoUpdater.checkForUpdatesAndNotify();
    }
}
let mainWindow: BrowserWindow | null = null;

ipcMain.on('ipc-example', async (event, arg) => {
    const msgTemplate = (pingPong: string) => `IPC test: ${pingPong}`;
    console.log(msgTemplate(arg));
    event.reply('ipc-example', msgTemplate('pong'));
});

if (process.env.NODE_ENV === 'production') {
    const sourceMapSupport = require('source-map-support');
    sourceMapSupport.install();
}

const isDevelopment =
    process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

const backend = execFile('./python/main.exe', (error, sout, stderr) => {
    stdout.write(`Python : ${sout}`);
    if (error) {
        console.error(stderr);
        throw error;
    }
    console.log(stdout);
});
if (isDevelopment) {
    require('electron-debug')();
}

const installExtensions = async () => {
    const installer = require('electron-devtools-installer');
    const forceDownload = !!process.env.UPGRADE_EXTENSIONS;
    const extensions = ['REACT_DEVELOPER_TOOLS'];

    return installer
        .default(
            extensions.map((name) => installer[name]),
            forceDownload
        )
        .catch(console.log);
};

const createWindow = async () => {
    if (isDevelopment) {
        await installExtensions();
    }

    const RESOURCES_PATH = app.isPackaged
        ? path.join(process.resourcesPath, 'assets')
        : path.join(__dirname, '../../assets');

    const getAssetPath = (...paths: string[]): string => {
        return path.join(RESOURCES_PATH, ...paths);
    };

    mainWindow = new BrowserWindow({
        show: false,
        width: 1024,
        height: 728,
        icon: getAssetPath('icon.png'),
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            webSecurity: false,
        },
    });

    mainWindow.loadURL(resolveHtmlPath('index.html'));

    mainWindow.on('ready-to-show', () => {
        if (!mainWindow) {
            throw new Error('"mainWindow" is not defined');
        }
        if (process.env.START_MINIMIZED) {
            mainWindow.minimize();
        } else {
            mainWindow.show();
        }
    });

    mainWindow.on('closed', () => {
        backend.kill('SIGTERM');
        mainWindow = null;
    });

    const menuBuilder = new MenuBuilder(mainWindow);
    menuBuilder.buildMenu();

    // Open urls in the user's browser
    mainWindow.webContents.on('new-window', (event, url) => {
        event.preventDefault();
        shell.openExternal(url);
    });
};

/**
 * Add event listeners...
 */

ipcMain.on('open-DevTools', () => {
    mainWindow?.openDevTools();
});

ipcMain.on('app-version', (e) => {
    e.returnValue = app.getVersion();
});

ipcMain.on('file-vault-set-destination', (e) => {
    const opts = {
        title: `Destination for File Vault`,

        defaultPath: 'C:\\Users\\%UserProfile%\\Desktop\\',

        buttonLabel: 'Select Folder',

        properties: ['openDirectory'],
    };

    dialog
        .showOpenDialog(opts)
        .then((file) => {
            // Stating whether dialog operation was cancelled or not.
            if (!file.canceled && file.filePaths.toString() !== '') {
                const folderPath = file.filePaths.toString();
                if (existsSync(`${folderPath}\\Vault`)) {
                    e.returnValue = JSON.stringify({
                        exists: true,
                        path: folderPath,
                    });
                } else {
                    e.returnValue = JSON.stringify({
                        exists: false,
                        path: folderPath,
                    });
                }
                return true;
            }
            return false;
        })
        .catch((err) => {
            // eslint-disable-next-line no-console
            console.error(err);
        });
});

app.on('window-all-closed', () => {
    // Respect the OSX convention of having the application in memory even
    // after all windows have been closed
    if (process.platform !== 'darwin') {
        app.quit();
        backend.kill('SIGINT');
    }
});

app.whenReady()
    .then(() => {
        createWindow();
        app.on('activate', () => {
            // On macOS it's common to re-create a window in the app when the
            // dock icon is clicked and there are no other windows open.
            if (mainWindow === null) createWindow();
        });
    })
    .catch(console.log);
