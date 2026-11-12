"""
SUNSCAN Permissions & Environment Detection
Organization: CodeSun
License: MIT
"""

import os
import platform
import shutil
import sys
from typing import Dict, Any


def is_root() -> bool:
    """Checks if the current process has root / superuser privileges."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        # Windows fallback
        return False


def is_termux() -> bool:
    """Detects if running inside Termux on Android."""
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or os.path.exists("/data/data/com.termux")


def detect_platform_details() -> Dict[str, Any]:
    """Inspects the local operating environment and returns telemetry details."""
    system = platform.system().lower()
    machine = platform.machine()
    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    distro_name = "unknown"
    if system == "linux":
        if is_termux():
            distro_name = "termux"
        elif os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith("ID="):
                            distro_name = line.strip().split("=")[1].strip('"\'')
                            break
            except Exception:
                distro_name = "linux"
        else:
            distro_name = "linux"
    elif system == "darwin":
        distro_name = "macos"

    # Detect package manager
    pkg_manager = None
    if is_termux() and shutil.which("pkg"):
        pkg_manager = "pkg"
    elif shutil.which("apt-get"):
        pkg_manager = "apt"
    elif shutil.which("pacman"):
        pkg_manager = "pacman"
    elif shutil.which("dnf"):
        pkg_manager = "dnf"
    elif shutil.which("yum"):
        pkg_manager = "yum"
    elif shutil.which("brew"):
        pkg_manager = "brew"

    return {
        "system": system,
        "distro": distro_name,
        "machine": machine,
        "is_root": is_root(),
        "is_termux": is_termux(),
        "python_version": python_ver,
        "package_manager": pkg_manager,
    }
