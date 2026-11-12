"""
SUNSCAN Configuration Manager
Organization: CodeSun
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "openrouter_api_key": "",
    "openrouter_model": "google/gemini-2.0-flash-001",
    "language": "en",  # "en" or "bn" (Bangla)
    "output_dir": "reports",
    "storage_dir": "storage",
    "max_output_lines": 5000,
    "timeout_seconds": 300,
    "auto_analyze_with_ai": False,
    "safe_mode": True,
}

CONFIG_FILE_PATH = Path(os.environ.get("SUNSCAN_CONFIG_PATH", Path.home() / ".sunscan" / "config.json"))


def load_config() -> Dict[str, Any]:
    """Loads SUNSCAN configuration from disk or returns default configuration."""
    if not CONFIG_FILE_PATH.exists():
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(saved)
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config_data: Dict[str, Any]) -> bool:
    """Saves updated configuration to disk."""
    try:
        CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        return True
    except Exception:
        return False


def get_config_value(key: str, default: Any = None) -> Any:
    cfg = load_config()
    return cfg.get(key, default if default is not None else DEFAULT_CONFIG.get(key))


def set_config_value(key: str, value: Any) -> bool:
    cfg = load_config()
    cfg[key] = value
    return save_config(cfg)
