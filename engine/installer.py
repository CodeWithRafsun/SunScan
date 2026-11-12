"""
SUNSCAN Independent Tool Installer
Organization: CodeSun
License: MIT
"""

import shutil
import subprocess
from typing import Dict, Any, List, Optional, Tuple

from engine.permissions import detect_platform_details, is_root


def get_install_command_for_tool(tool: Dict[str, Any]) -> Optional[List[str]]:
    """
    Determines the appropriate verified installation command for the target tool
    based on the host platform's detected package manager.
    """
    env = detect_platform_details()
    pkg_mgr = env.get("package_manager")
    executable = tool.get("executable")
    tool_id = tool.get("id")

    # Map package names if they differ from tool executable
    apt_names = {
        "whatweb": "whatweb",
        "nmap": "nmap",
        "nikto": "nikto",
        "sqlmap": "sqlmap",
        "feroxbuster": "feroxbuster",
        "dirsearch": "dirsearch",
        "gobuster": "gobuster",
        "ffuf": "ffuf",
        "subfinder": "subfinder",
        "dnsrecon": "dnsrecon",
        "testssl": "testssl.sh",
        "sslyze": "sslyze",
        "nuclei": "nuclei",
        "theharvester": "theharvester",
        "sherlock": "sherlock",
        "semgrep": "semgrep",
    }

    pkg_name = apt_names.get(tool_id, executable)

    if pkg_mgr == "pkg":  # Termux
        return ["pkg", "install", "-y", pkg_name]
    elif pkg_mgr == "apt":
        prefix = [] if is_root() else ["sudo"]
        return prefix + ["apt-get", "install", "-y", pkg_name]
    elif pkg_mgr == "pacman":
        prefix = [] if is_root() else ["sudo"]
        return prefix + ["pacman", "-S", "--noconfirm", pkg_name]
    elif pkg_mgr in ("dnf", "yum"):
        prefix = [] if is_root() else ["sudo"]
        return prefix + [pkg_mgr, "install", "-y", pkg_name]
    elif pkg_mgr == "brew":
        return ["brew", "install", pkg_name]

    return None


def get_manual_instructions(tool: Dict[str, Any]) -> str:
    """Returns manual installation guidance when package manager auto-install is unavailable."""
    tool_name = tool.get("name", "Tool")
    repo = tool.get("repository", "official repository")
    installers = ", ".join(tool.get("installers", ["package manager"]))
    return (
        f"Manual Installation Instructions for {tool_name}:\n"
        f"  1. Visit official repository: {repo}\n"
        f"  2. Supported installation methods: {installers}\n"
        f"  3. Common manual commands:\n"
        f"     - Debian/Kali: sudo apt-get install {tool.get('executable')}\n"
        f"     - Python (if applicable): pip install {tool.get('executable')}\n"
        f"     - Go (if applicable): go install <repository>@latest\n"
        f"     - Termux: pkg install {tool.get('executable')}\n"
    )


def execute_tool_installation(tool: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Executes tool installation via the detected package manager.
    Note: Must be preceded by explicit user confirmation in the calling CLI/UI layer.
    """
    cmd = get_install_command_for_tool(tool)
    if not cmd:
        return False, "No compatible package manager detected on this system. Please install manually."

    cmd_str = " ".join(cmd)
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )
        if proc.returncode == 0:
            # Verify if executable is now in PATH
            executable = tool.get("executable")
            if executable and shutil.which(executable):
                return True, f"Successfully installed {tool.get('name')}."
            return True, f"Installation process completed for {tool.get('name')} (Command: {cmd_str})."
        else:
            return False, f"Installation failed with exit code {proc.returncode}:\n{proc.stderr}"
    except subprocess.TimeoutExpired:
        return False, f"Installation timed out after 300 seconds."
    except Exception as e:
        return False, f"Installation error: {str(e)}"
