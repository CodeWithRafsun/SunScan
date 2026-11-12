"""
SUNSCAN Safe Process Execution Engine
Organization: CodeSun
License: MIT
"""

import os
import signal
import subprocess
import time
import uuid
from datetime import datetime
from typing import Callable, Dict, Any, List, Optional, Tuple

from engine.validator import validate_target, contains_unsafe_shell_characters


class ScanJob:
    def __init__(
        self,
        tool_id: str,
        command_id: str,
        target: str,
        args_array: List[str],
        scan_id: Optional[str] = None,
        timeout: int = 300,
    ):
        self.scan_id = scan_id or f"scan-{uuid.uuid4().hex[:10]}"
        self.tool_id = tool_id
        self.command_id = command_id
        self.target = target
        self.args_array = args_array
        self.timeout = timeout
        self.status = "pending"  # pending, running, completed, failed, cancelled, timed_out
        self.start_time: Optional[str] = None
        self.end_time: Optional[str] = None
        self.duration_seconds: float = 0.0
        self.exit_code: Optional[int] = None
        self.output_lines: List[str] = []
        self.error_message: Optional[str] = None
        self.process: Optional[subprocess.Popen] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "tool_id": self.tool_id,
            "command_id": self.command_id,
            "target": self.target,
            "command": " ".join(self.args_array),
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": round(self.duration_seconds, 2),
            "exit_code": self.exit_code,
            "output_lines_count": len(self.output_lines),
            "raw_output": "\n".join(self.output_lines),
            "error_message": self.error_message,
        }


def build_command_args(
    tool: Dict[str, Any], command_preset: Dict[str, Any], target: str
) -> Tuple[bool, List[str], str]:
    """
    Constructs a safe, non-shell argument list for execution.
    Returns: (is_safe, args_array, error_message)
    """
    is_valid, target_type, normalized_target = validate_target(target)
    if not is_valid:
        return False, [], f"Invalid target: {normalized_target}"

    executable = tool.get("executable")
    if not executable:
        return False, [], "Tool has no executable defined."

    args = [executable]
    for arg in command_preset.get("args", []):
        if "{target}" in arg:
            args.append(arg.replace("{target}", normalized_target))
        else:
            args.append(arg)

    # If the preset template had {target} at the end rather than in args array
    if not any(normalized_target in a for a in args):
        args.append(normalized_target)

    # Double-check for any shell injection attempts in all arguments
    for a in args:
        if contains_unsafe_shell_characters(a):
            return False, [], f"Unsafe characters detected in argument: {a}"

    return True, args, ""


def execute_scan(
    job: ScanJob,
    on_output_line: Optional[Callable[[str], None]] = None,
) -> ScanJob:
    """
    Executes the scan job safely using subprocess.Popen without shell=True.
    Streams output lines in real time if a callback is provided.
    """
    job.status = "running"
    job.start_time = datetime.utcnow().isoformat() + "Z"
    start_ts = time.time()

    try:
        proc = subprocess.Popen(
            job.args_array,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            preexec_fn=os.setsid if hasattr(os, "setsid") else None,
        )
        job.process = proc

        max_lines = 10000
        line_count = 0

        while True:
            # Check for timeout
            if time.time() - start_ts > job.timeout:
                job.status = "timed_out"
                job.error_message = f"Scan exceeded maximum execution timeout of {job.timeout}s."
                _kill_process_tree(proc)
                break

            line = proc.stdout.readline() if proc.stdout else ""
            if not line and proc.poll() is not None:
                break

            if line:
                cleaned_line = line.rstrip("\r\n")
                if line_count < max_lines:
                    job.output_lines.append(cleaned_line)
                    line_count += 1
                if on_output_line:
                    on_output_line(cleaned_line)

        proc.wait(timeout=5)
        job.exit_code = proc.returncode

        if job.status == "running":
            job.status = "completed" if proc.returncode == 0 else "failed"

    except subprocess.TimeoutExpired:
        job.status = "timed_out"
        job.error_message = f"Process timed out after {job.timeout} seconds."
        if job.process:
            _kill_process_tree(job.process)
    except FileNotFoundError:
        job.status = "failed"
        job.error_message = f"Executable '{job.args_array[0]}' not found in system PATH."
    except Exception as e:
        job.status = "failed"
        job.error_message = f"Execution exception: {str(e)}"

    job.end_time = datetime.utcnow().isoformat() + "Z"
    job.duration_seconds = time.time() - start_ts
    return job


def cancel_scan(job: ScanJob) -> bool:
    """Cancels an active scan job."""
    if job.process and job.status == "running":
        job.status = "cancelled"
        _kill_process_tree(job.process)
        job.end_time = datetime.utcnow().isoformat() + "Z"
        return True
    return False


def _kill_process_tree(proc: subprocess.Popen) -> None:
    try:
        if hasattr(os, "killpg") and hasattr(os, "getpgid"):
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        else:
            proc.terminate()
        time.sleep(0.5)
        if proc.poll() is None:
            if hasattr(os, "killpg") and hasattr(os, "getpgid"):
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            else:
                proc.kill()
    except Exception:
        pass
