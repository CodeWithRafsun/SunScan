"""
SUNSCAN Tool Registry
Organization: CodeSun
License: MIT
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

CATALOG_PATH = Path(__file__).resolve().parent.parent / "docs" / "TOOL_CATALOG.json"


class ToolRegistry:
    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path = catalog_path or CATALOG_PATH
        self._catalog_data: Dict[str, Any] = {}
        self._categories: List[Dict[str, Any]] = []
        self._tools: Dict[str, Dict[str, Any]] = {}
        self.load_catalog()

    def load_catalog(self) -> bool:
        if not self.catalog_path.exists():
            return False
        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                self._catalog_data = json.load(f)
                self._categories = self._catalog_data.get("categories", [])
                for t in self._catalog_data.get("tools", []):
                    self._tools[t["id"]] = t
            return True
        except Exception:
            return False

    def get_categories(self) -> List[Dict[str, Any]]:
        return self._categories

    def get_category_by_id(self, category_id: str) -> Optional[Dict[str, Any]]:
        for cat in self._categories:
            if cat["id"] == category_id:
                return cat
        return None

    def get_tools_for_category(self, category_id: str) -> List[Dict[str, Any]]:
        return [t for t in self._tools.values() if t.get("category") == category_id]

    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(tool_id)

    def is_tool_installed(self, tool_id: str) -> bool:
        tool = self.get_tool(tool_id)
        if not tool:
            return False
        executable = tool.get("executable")
        if not executable:
            return False
        return shutil.which(executable) is not None

    def get_tool_executable_path(self, tool_id: str) -> Optional[str]:
        tool = self.get_tool(tool_id)
        if not tool:
            return None
        executable = tool.get("executable")
        if not executable:
            return None
        return shutil.which(executable)

    def get_all_tools(self) -> List[Dict[str, Any]]:
        return list(self._tools.values())


# Global singleton
registry = ToolRegistry()
