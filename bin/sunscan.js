#!/usr/bin/env node
/**
 * SUNSCAN CLI Executable Wrapper
 * Package: sunscan-cli
 * Command: sunscan
 * Organization: CodeSun
 * License: MIT
 */

import { launchSunscan } from '../src/launcher.js';

const cliArgs = process.argv.slice(2);
launchSunscan(cliArgs);
