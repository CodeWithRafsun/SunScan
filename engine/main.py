#!/usr/bin/env python3
"""
SUNSCAN - Modular Cybersecurity Toolkit & AI-Powered Output Analyzer
Organization: CodeSun
License: MIT
Entry Point: engine/main.py
"""

import argparse
import sys
from pathlib import Path

# Ensure root directory is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from engine.cli import run_cli_loop, console
from engine.registry import registry
from engine.permissions import detect_platform_details
from engine.validator import validate_target
from engine.executor import build_command_args, execute_scan, ScanJob
from engine.process_manager import process_manager
from ai.analyzer import analyze_scan

VERSION = "1.0.0"


def main():
    parser = argparse.ArgumentParser(
        prog="sunscan",
        description="SUNSCAN: Modular Cybersecurity Toolkit & AI-Powered Output Analyzer by CodeSun.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"SUNSCAN v{VERSION} (CodeSun)")
    parser.add_argument("--diag", action="store_true", help="Print system environment and package manager diagnostics.")
    parser.add_argument("--list-tools", action="store_true", help="List all registered tools in the catalog.")
    parser.add_argument("--scan", nargs=2, metavar=("TOOL", "TARGET"), help="Run a quick non-interactive scan: sunscan --scan <tool_id> <target>")
    parser.add_argument("--ai", action="store_true", help="Automatically trigger AI analysis on completed scan.")
    parser.add_argument("--lang", choices=["en", "bn"], default="en", help="Language for output (en: English, bn: Bangla).")

    args = parser.parse_args()

    if args.diag:
        env = detect_platform_details()
        print("SUNSCAN System Diagnostics:")
        for k, v in env.items():
            print(f"  {k}: {v}")
        sys.exit(0)

    if args.list_tools:
        tools = registry.get_all_tools()
        print(f"Registered Tools ({len(tools)} total):")
        for t in tools:
            inst = "[INSTALLED]" if registry.is_tool_installed(t["id"]) else "[MISSING]"
            print(f"  {t['id']:<15} {inst:<12} {t['name']:<18} ({t['category']})")
        sys.exit(0)

    if args.scan:
        tool_id, target = args.scan
        tool = registry.get_tool(tool_id)
        if not tool:
            print(f"Error: Tool '{tool_id}' not found in SUNSCAN catalog.", file=sys.stderr)
            sys.exit(1)

        if not registry.is_tool_installed(tool_id):
            print(f"Error: Tool '{tool_id}' is not installed on this system.", file=sys.stderr)
            print(f"Run `sunscan` interactively or install via your package manager.", file=sys.stderr)
            sys.exit(1)

        is_valid, _, normalized = validate_target(target)
        if not is_valid:
            print(f"Error: Invalid target '{target}' ({normalized})", file=sys.stderr)
            sys.exit(1)

        commands = tool.get("commands", [])
        if not commands:
            print(f"Error: No default command presets found for tool '{tool_id}'.", file=sys.stderr)
            sys.exit(1)

        default_preset = commands[0]
        is_safe, cmd_args, err = build_command_args(tool, default_preset, normalized)
        if not is_safe:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)

        print(f"Executing: {' '.join(cmd_args)}")
        job = ScanJob(tool_id=tool_id, command_id=default_preset["id"], target=normalized, args_array=cmd_args)
        execute_scan(job, on_output_line=lambda line: print(line))
        process_manager.save_job_to_disk(job)

        if args.ai:
            print("\nAnalyzing output...")
            result = analyze_scan(tool["name"], normalized, job.to_dict()["raw_output"], use_ai=True, language=args.lang)
            print(f"\nSummary: {result.get('summary')}")
            print(f"Risk: {result.get('risk_score')}")
        sys.exit(job.exit_code or 0)

    # If no flags provided, launch interactive Rich/Questionary interface
    try:
        run_cli_loop()
    except (KeyboardInterrupt, EOFError):
        print("\nSUNSCAN terminated.")
        sys.exit(0)


if __name__ == "__main__":
    main()
