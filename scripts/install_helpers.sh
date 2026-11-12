#!/bin/sh
# SUNSCAN Tool Installation Helper
# Organization: CodeSun
# License: MIT
# Note: Never run blindly; this helper is called with explicit tool parameter and user approval.

set -e

TOOL_NAME="$1"

if [ -z "$TOOL_NAME" ]; then
    echo "Usage: $0 <tool_executable_or_name>"
    exit 1
fi

echo "[SUNSCAN] Verifying installation status for '$TOOL_NAME'..."

if command -v "$TOOL_NAME" >/dev/null 2>&1; then
    echo "[SUNSCAN] Tool '$TOOL_NAME' is already installed at: $(command -v "$TOOL_NAME")"
    exit 0
fi

echo "[SUNSCAN] Tool '$TOOL_NAME' is not currently installed."

# Detect package manager
if [ -n "$PREFIX" ] && command -v pkg >/dev/null 2>&1; then
    echo "[SUNSCAN] Suggested Termux install command: pkg install -y $TOOL_NAME"
elif command -v apt-get >/dev/null 2>&1; then
    echo "[SUNSCAN] Suggested Debian/Ubuntu/Kali install command: sudo apt-get install -y $TOOL_NAME"
elif command -v pacman >/dev/null 2>&1; then
    echo "[SUNSCAN] Suggested Arch install command: sudo pacman -S --noconfirm $TOOL_NAME"
elif command -v dnf >/dev/null 2>&1; then
    echo "[SUNSCAN] Suggested Fedora install command: sudo dnf install -y $TOOL_NAME"
elif command -v brew >/dev/null 2>&1; then
    echo "[SUNSCAN] Suggested Homebrew install command: brew install $TOOL_NAME"
else
    echo "[SUNSCAN] No automatic package manager detected. Please refer to official project documentation."
fi
