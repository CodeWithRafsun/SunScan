#!/bin/sh
# SUNSCAN POSIX Environment Detector
# Organization: CodeSun
# License: MIT

set -e

echo "=== SUNSCAN System Environment Telemetry ==="

# OS detection
OS="$(uname -s 2>/dev/null || echo 'Unknown')"
ARCH="$(uname -m 2>/dev/null || echo 'Unknown')"
echo "Operating System: $OS"
echo "Architecture: $ARCH"

# Detect Termux
if [ -n "$PREFIX" ] && [ -d "$PREFIX" ] && echo "$PREFIX" | grep -q "com.termux"; then
    IS_TERMUX=1
    echo "Environment: Android Termux Userland"
else
    IS_TERMUX=0
    echo "Environment: Standard Host"
fi

# Detect package managers
PKG_MGR="none"
if [ "$IS_TERMUX" -eq 1 ] && command -v pkg >/dev/null 2>&1; then
    PKG_MGR="pkg (Termux)"
elif command -v apt-get >/dev/null 2>&1; then
    PKG_MGR="apt (Debian/Ubuntu/Kali)"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MGR="pacman (Arch/BlackArch)"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MGR="dnf (Fedora)"
elif command -v brew >/dev/null 2>&1; then
    PKG_MGR="brew (macOS/Linux)"
fi
echo "Detected Package Manager: $PKG_MGR"

# Detect Python 3
if command -v python3 >/dev/null 2>&1; then
    PY_VER="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')"
    echo "Python 3: Installed ($PY_VER)"
else
    echo "Python 3: NOT FOUND (Required for SUNSCAN engine)"
fi

# Detect Node.js
if command -v node >/dev/null 2>&1; then
    NODE_VER="$(node -v)"
    echo "Node.js: Installed ($NODE_VER)"
else
    echo "Node.js: NOT FOUND"
fi

echo "============================================="
