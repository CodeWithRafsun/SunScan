/**
 * SUNSCAN Python Engine Launcher for Node.js
 * Organization: CodeSun
 * License: MIT
 */

import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const MAIN_PY_PATH = path.join(ROOT_DIR, 'engine', 'main.py');

export function checkPythonInstalled() {
  return new Promise((resolve) => {
    const checker = spawn('python3', ['--version'], { stdio: 'ignore' });
    checker.on('error', () => resolve(false));
    checker.on('close', (code) => resolve(code === 0));
  });
}

export async function launchSunscan(args = []) {
  const hasPython = await checkPythonInstalled();
  if (!hasPython) {
    console.error('\x1b[31m[SUNSCAN ERROR]\x1b[0m Python 3 was not found in your system PATH.');
    console.error('SUNSCAN core execution engine requires Python 3.8 or higher.');
    console.error('\nPlease install Python 3:');
    console.error('  - Debian/Ubuntu/Kali: sudo apt-get install python3 python3-pip');
    console.error('  - Termux (Android):   pkg install python');
    console.error('  - macOS:              brew install python');
    process.exit(1);
  }

  const child = spawn('python3', [MAIN_PY_PATH, ...args], {
    stdio: 'inherit',
    env: {
      ...process.env,
      PYTHONUNBUFFERED: '1',
    },
  });

  child.on('error', (err) => {
    console.error('\x1b[31m[SUNSCAN ERROR]\x1b[0m Failed to spawn SUNSCAN Python engine:', err.message);
    process.exit(1);
  });

  child.on('close', (code) => {
    process.exit(code ?? 0);
  });
}
