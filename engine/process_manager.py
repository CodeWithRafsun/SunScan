"""
SUNSCAN Process & History Manager
Organization: CodeSun
License: MIT
"""

import json
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional

from engine.executor import ScanJob, execute_scan, cancel_scan

STORAGE_DIR = Path(__file__).resolve().parent.parent / "storage" / "scans"


class ProcessManager:
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or STORAGE_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.active_jobs: Dict[str, ScanJob] = {}
        self._lock = threading.Lock()

    def start_background_scan(self, job: ScanJob) -> str:
        """Launches a scan job in a detached background thread."""
        with self._lock:
            self.active_jobs[job.scan_id] = job

        def run_target():
            execute_scan(job)
            self.save_job_to_disk(job)

        thread = threading.Thread(target=run_target, daemon=True)
        thread.start()
        return job.scan_id

    def get_job_status(self, scan_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if scan_id in self.active_jobs:
                return self.active_jobs[scan_id].to_dict()

        # Check disk if not in memory
        saved_file = self.storage_dir / f"{scan_id}.json"
        if saved_file.exists():
            try:
                with open(saved_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def cancel_active_scan(self, scan_id: str) -> bool:
        with self._lock:
            if scan_id in self.active_jobs:
                return cancel_scan(self.active_jobs[scan_id])
        return False

    def save_job_to_disk(self, job: ScanJob) -> bool:
        try:
            target_file = self.storage_dir / f"{job.scan_id}.json"
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(job.to_dict(), f, indent=2)
            return True
        except Exception:
            return False

    def list_recent_scans(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Lists completed or persisted scans from disk."""
        results = []
        if not self.storage_dir.exists():
            return results

        files = sorted(self.storage_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        for f in files[:limit]:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    results.append(json.load(fp))
            except Exception:
                continue
        return results


# Global process manager
process_manager = ProcessManager()
