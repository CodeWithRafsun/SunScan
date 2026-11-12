/**
 * SUNSCAN Platform Detection in Node.js
 * Organization: CodeSun
 * License: MIT
 */

import os from 'node:os';
import fs from 'node:fs';

export function getSystemInfo() {
  const platform = os.platform();
  const arch = os.arch();
  const isTermux = Boolean(process.env.PREFIX && process.env.PREFIX.includes('com.termux'));

  let distro = platform;
  if (platform === 'linux') {
    if (isTermux) {
      distro = 'termux';
    } else if (fs.existsSync('/etc/os-release')) {
      try {
        const content = fs.readFileSync('/etc/os-release', 'utf8');
        const match = content.match(/^ID=(.*)$/m);
        if (match) {
          distro = match[1].replace(/["']/g, '');
        }
      } catch {
        distro = 'linux';
      }
    }
  }

  return {
    platform,
    arch,
    isTermux,
    distro,
    nodeVersion: process.version,
  };
}
