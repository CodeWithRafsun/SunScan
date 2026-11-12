"""
SUNSCAN Terminal CLI Interface
Organization: CodeSun
License: MIT
"""

import sys
import time
from typing import Dict, Any, List, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import print as rprint
except ImportError:
    # Graceful standard console fallback if rich is not yet installed
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    def rprint(*args, **kwargs):
        print(*args)

console = Console()

from engine.registry import registry
from engine.config import load_config, save_config, get_config_value, set_config_value
from engine.permissions import detect_platform_details
from engine.installer import get_install_command_for_tool, get_manual_instructions, execute_tool_installation
from engine.validator import validate_target
from engine.executor import build_command_args, execute_scan, ScanJob
from engine.process_manager import process_manager
from ai.openrouter import OpenRouterClient, POPULAR_MODELS
from ai.analyzer import analyze_scan


ASCII_BANNER = """
[bold yellow]╔════════════════════════════════════════════════════╗[/bold yellow]
[bold yellow]║[/bold yellow]                                                    [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow]                      [bold white]SUNSCAN[/bold white]                       [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow]           [bold cyan]CYBERSECURITY TOOLKIT & ANALYZER[/bold cyan]         [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow]                                                    [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow]                 [bold green]A CODESUN PROJECT[/bold green]                  [bold yellow]║[/bold yellow]
[bold yellow]║[/bold yellow]                                                    [bold yellow]║[/bold yellow]
[bold yellow]╚════════════════════════════════════════════════════╝[/bold yellow]
[italic dim cyan]"Understand Every Scan. Discover Every Risk."[/italic dim cyan]
"""


def display_main_menu(lang: str = "en") -> str:
    console.print(ASCII_BANNER)
    categories = registry.get_categories()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold cyan", width=6)
    table.add_column("Category", style="bold white")

    idx = 1
    for cat in categories:
        name = cat["name"] if lang == "en" else f"{cat['name']} ({cat.get('bangla_name', '')})"
        table.add_row(f"[{idx:02d}]", name)
        idx += 1

    console.print(table)
    console.print("")

    mgmt_table = Table(show_header=False, box=None, padding=(0, 2))
    mgmt_table.add_column("Key", style="bold yellow", width=6)
    mgmt_table.add_column("Action", style="bold white")
    mgmt_table.add_row("[21]", "Tool Manager & Status" if lang == "en" else "টুল ম্যানেজার ও স্ট্যাটাস")
    mgmt_table.add_row("[22]", "Scan History" if lang == "en" else "স্ক্যান হিস্ট্রি")
    mgmt_table.add_row("[23]", "Reports" if lang == "en" else "রিপোর্টসমূহ")
    mgmt_table.add_row("[24]", "OpenRouter & AI Configuration" if lang == "en" else "ওপেনরাউটার ও এআই কনফিগারেশন")
    mgmt_table.add_row("[25]", "System Diagnostics" if lang == "en" else "সিস্টেম ডায়াগনস্টিকস")
    mgmt_table.add_row("[26]", f"Switch Language (Current: {lang.upper()})" if lang == "en" else f"ভাষা পরিবর্তন (বর্তমান: {lang.upper()})")
    mgmt_table.add_row("[00]", "Exit" if lang == "en" else "প্রস্থান")

    console.print(mgmt_table)
    console.print("")
    choice = input("sunscan > ").strip()
    return choice


def run_cli_loop():
    while True:
        cfg = load_config()
        lang = cfg.get("language", "en")
        choice = display_main_menu(lang)

        if choice in ("0", "00", "exit", "quit"):
            console.print("[dim]Exiting SUNSCAN. Stay safe and audit responsibly.[/dim]")
            sys.exit(0)

        elif choice == "21":
            _handle_tool_manager(lang)
        elif choice == "22":
            _handle_scan_history(lang)
        elif choice == "23":
            _handle_reports(lang)
        elif choice == "24":
            _handle_ai_config(lang)
        elif choice == "25":
            _handle_diagnostics(lang)
        elif choice == "26":
            new_lang = "bn" if lang == "en" else "en"
            set_config_value("language", new_lang)
            console.print(f"[green]Language switched to {new_lang.upper()}![/green]\n")
        else:
            try:
                cat_idx = int(choice) - 1
                categories = registry.get_categories()
                if 0 <= cat_idx < len(categories):
                    _handle_category_workflow(categories[cat_idx], lang)
                else:
                    console.print("[red]Invalid selection. Please choose an option from the menu.[/red]\n")
            except ValueError:
                console.print("[red]Please enter a valid menu number.[/red]\n")


def _handle_category_workflow(category: Dict[str, Any], lang: str):
    cat_id = category["id"]
    cat_name = category["name"] if lang == "en" else category.get("bangla_name", category["name"])
    tools = registry.get_tools_for_category(cat_id)

    if not tools:
        console.print(f"[yellow]No tools registered in catalog for category: {cat_name}[/yellow]\n")
        return

    console.print(f"\n[bold cyan]SUNSCAN / {cat_name.upper()}[/bold cyan]")
    for i, t in enumerate(tools, start=1):
        installed = registry.is_tool_installed(t["id"])
        status = "[bold green][Installed][/bold green]" if installed else "[bold red][Not Installed][/bold red]"
        console.print(f"[{i:02d}] {t['name']} {status} - {t['description']}")
    console.print("[00] Back")

    choice = input(f"sunscan/{cat_id} > ").strip()
    if choice in ("0", "00", "back"):
        return

    try:
        t_idx = int(choice) - 1
        if 0 <= t_idx < len(tools):
            _handle_tool_workflow(tools[t_idx], lang)
    except ValueError:
        pass


def _handle_tool_workflow(tool: Dict[str, Any], lang: str):
    tool_id = tool["id"]
    tool_name = tool["name"]
    is_installed = registry.is_tool_installed(tool_id)

    console.print(f"\n[bold cyan]SUNSCAN / {tool_name.upper()}[/bold cyan]")
    console.print(f"Description: {tool.get('description', '')}")
    if lang == "bn" and tool.get("bangla_description"):
        console.print(f"বিবরণ: {tool.get('bangla_description')}")
    console.print(f"Official Repository: {tool.get('repository')}")
    console.print(f"Executable: [bold]{tool.get('executable')}[/bold] | Status: {'[green]Installed[/green]' if is_installed else '[red]Not Installed[/red]'}")
    console.print("")

    if is_installed:
        console.print("[1] Open Command Catalog" if lang == "en" else "[1] কমান্ড ক্যাটালগ খুলুন")
        console.print("[2] Check Version" if lang == "en" else "[2] ভার্সন চেক")
        console.print("[0] Back" if lang == "en" else "[0] পেছনে যান")
        choice = input(f"sunscan/{tool_id} > ").strip()
        if choice == "1":
            _handle_command_catalog(tool, lang)
        elif choice == "2":
            _check_tool_version(tool)
    else:
        console.print("[1] Install Tool (Prompts confirmation)" if lang == "en" else "[1] টুল ইনস্টল করুন (সম্মতি চাওয়া হবে)")
        console.print("[2] View Manual Installation Instructions" if lang == "en" else "[2] ম্যানুয়াল ইনস্টলেশন নির্দেশিকা")
        console.print("[3] Check Platform Compatibility" if lang == "en" else "[3] প্ল্যাটফর্ম উপযুক্ততা যাচাই")
        console.print("[0] Back" if lang == "en" else "[0] পেছনে যান")
        choice = input(f"sunscan/{tool_id} > ").strip()
        if choice == "1":
            _prompt_and_install_tool(tool, lang)
        elif choice == "2":
            console.print("\n" + get_manual_instructions(tool))
        elif choice == "3":
            console.print(f"\nPlatforms: {', '.join(tool.get('platforms', []))}")
            console.print(f"Installers: {', '.join(tool.get('installers', []))}")
            console.print(f"Requires Root: {tool.get('requires_root', False)}\n")


def _handle_command_catalog(tool: Dict[str, Any], lang: str):
    commands = tool.get("commands", [])
    if not commands:
        console.print("[yellow]No presets defined for this tool.[/yellow]\n")
        return

    console.print(f"\n[bold cyan]COMMAND CATALOG: {tool['name'].upper()}[/bold cyan]")
    for i, cmd in enumerate(commands, start=1):
        level_badge = f"[{cmd.get('level', 'basic').upper()}]"
        risk_color = "green" if cmd.get("risk") == "low" else ("yellow" if cmd.get("risk") == "medium" else "red")
        risk_badge = f"[{risk_color}][{cmd.get('risk', 'low').upper()} RISK][/{risk_color}]"
        name = cmd["name"]
        console.print(f"[{i:02d}] {name} {level_badge} {risk_badge}")
        purpose = cmd["purpose"] if lang == "en" else cmd.get("bangla_purpose", cmd["purpose"])
        console.print(f"     [dim]{purpose}[/dim]")
    console.print("[00] Back")

    choice = input(f"sunscan/{tool['id']}/commands > ").strip()
    if choice in ("0", "00", "back"):
        return

    try:
        c_idx = int(choice) - 1
        if 0 <= c_idx < len(commands):
            _handle_execution_workflow(tool, commands[c_idx], lang)
    except ValueError:
        pass


def _handle_execution_workflow(tool: Dict[str, Any], cmd_preset: Dict[str, Any], lang: str):
    console.print(f"\n[bold cyan]COMMAND DETAILS: {cmd_preset['name']}[/bold cyan]")
    console.print(f"Purpose: {cmd_preset.get('purpose')}")
    console.print(f"Template: [bold yellow]{cmd_preset.get('command_template')}[/bold yellow]")
    console.print(f"Risk Level: {cmd_preset.get('risk', 'low').upper()} | Estimated Time: {cmd_preset.get('time_estimate', '1-2m')}")
    console.print(f"[bold red]AUTHORIZATION NOTICE:[/bold red] {cmd_preset.get('authorization_notice')}")
    console.print("")

    target = input("Enter target (Hostname, IPv4, URL, or CIDR): ").strip()
    if not target:
        console.print("[red]Target cannot be empty.[/red]\n")
        return

    is_valid, target_type, normalized = validate_target(target)
    if not is_valid:
        console.print(f"[red]Validation failed: {normalized}[/red]\n")
        return

    is_safe, args, err = build_command_args(tool, cmd_preset, normalized)
    if not is_safe:
        console.print(f"[red]Safety check failed: {err}[/red]\n")
        return

    command_str = " ".join(args)
    console.print(f"\nConstructed Command: [bold green]{command_str}[/bold green]")
    console.print("[yellow]WARNING: Only scan systems you own or are explicitly authorized to audit.[/yellow]")
    confirm = input("Confirm execution? (y/N): ").strip().lower()
    if confirm != "y":
        console.print("[dim]Scan aborted by user.[/dim]\n")
        return

    job = ScanJob(tool_id=tool["id"], command_id=cmd_preset["id"], target=normalized, args_array=args)

    console.print("\n[bold green]Scan starting... Streaming live output:[/bold green]\n")
    execute_scan(job, on_output_line=lambda line: console.print(f"[dim]{line}[/dim]"))

    console.print(f"\n[bold]Scan Finished![/bold] Status: [bold]{job.status.upper()}[/bold] (Duration: {job.duration_seconds:.2f}s, Exit Code: {job.exit_code})")
    process_manager.save_job_to_disk(job)

    # Prompt for AI analysis
    ask_ai = input("\nPerform AI / Heuristic analysis on this scan output? (Y/n): ").strip().lower()
    if ask_ai != "n":
        console.print("[cyan]Analyzing scan output...[/cyan]")
        analysis = analyze_scan(tool["name"], normalized, job.to_dict()["raw_output"], use_ai=True, language=lang)
        console.print("\n" + "=" * 60)
        console.print(f"[bold green]SUMMARY:[/bold green] {analysis.get('summary')}")
        console.print(f"[bold]Risk Score:[/bold] {analysis.get('risk_score', 'low').upper()}")
        console.print("=" * 60)
        findings = analysis.get("findings", [])
        if findings:
            for f in findings:
                sev = f.get("severity", "low").upper()
                console.print(f"\n• [bold red][{sev}][/bold red] {f.get('title')}")
                console.print(f"  Explanation: {f.get('explanation')}")
                console.print(f"  Evidence: [italic dim]{f.get('evidence')}[/italic dim]")
                console.print(f"  Remediation: [green]{f.get('recommendation')}[/green]")
        else:
            console.print("[green]No high-risk vulnerabilities or misconfigurations discovered.[/green]")
        console.print("\n" + "=" * 60 + "\n")


def _check_tool_version(tool: Dict[str, Any]):
    import subprocess
    executable = tool.get("executable")
    try:
        res = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
        out = (res.stdout or res.stderr).strip().splitlines()[0] if (res.stdout or res.stderr) else "Installed (no version flag)"
        console.print(f"[green]{tool['name']} version:[/green] {out}\n")
    except Exception as e:
        console.print(f"[yellow]Could not determine version: {e}[/yellow]\n")


def _prompt_and_install_tool(tool: Dict[str, Any], lang: str):
    cmd = get_install_command_for_tool(tool)
    if not cmd:
        console.print("[red]No supported package manager found. Please use manual installation.[/red]")
        console.print(get_manual_instructions(tool))
        return

    cmd_str = " ".join(cmd)
    console.print(f"\nProposed Installation Command: [bold yellow]{cmd_str}[/bold yellow]")
    confirm = input(f"Do you want to install {tool['name']} now? (y/N): ").strip().lower()
    if confirm != "y":
        console.print("[dim]Installation aborted.[/dim]\n")
        return

    console.print(f"[cyan]Installing {tool['name']}... please wait...[/cyan]")
    success, msg = execute_tool_installation(tool)
    if success:
        console.print(f"[bold green]SUCCESS:[/bold green] {msg}\n")
    else:
        console.print(f"[bold red]FAILED:[/bold red] {msg}\n")


def _handle_tool_manager(lang: str):
    console.print("\n[bold cyan]SUNSCAN TOOL MANAGER & INVENTORY[/bold cyan]")
    tools = registry.get_all_tools()
    table = Table(title="Cybersecurity Tool Catalog Status", show_header=True)
    table.add_column("Tool", style="bold")
    table.add_column("Category")
    table.add_column("Status")
    table.add_column("Path / Installers")

    for t in tools:
        is_inst = registry.is_tool_installed(t["id"])
        status = "[green]Installed[/green]" if is_inst else "[red]Missing[/red]"
        path = registry.get_tool_executable_path(t["id"]) or ", ".join(t.get("installers", []))
        table.add_row(t["name"], t["category"], status, path)

    console.print(table)
    console.print("")


def _handle_scan_history(lang: str):
    console.print("\n[bold cyan]RECENT SCAN HISTORY[/bold cyan]")
    scans = process_manager.list_recent_scans(limit=10)
    if not scans:
        console.print("[dim]No scan records found in local storage.[/dim]\n")
        return

    table = Table(show_header=True)
    table.add_column("Scan ID", style="bold cyan")
    table.add_column("Tool")
    table.add_column("Target")
    table.add_column("Status")
    table.add_column("Duration")
    table.add_column("Timestamp")

    for s in scans:
        status_color = "green" if s.get("status") == "completed" else "yellow"
        table.add_row(
            s.get("scan_id", ""),
            s.get("tool_id", ""),
            s.get("target", ""),
            f"[{status_color}]{s.get('status')}[/{status_color}]",
            f"{s.get('duration_seconds', 0)}s",
            s.get("start_time", "")[:19],
        )
    console.print(table)
    console.print("")


def _handle_reports(lang: str):
    console.print("\n[bold cyan]REPORT MANAGEMENT[/bold cyan]")
    scans = process_manager.list_recent_scans(limit=5)
    console.print(f"Total reports stored: {len(scans)}")
    console.print("Reports are stored in JSON and exportable to HTML from the SUNSCAN Web Workbench.\n")


def _handle_ai_config(lang: str):
    cfg = load_config()
    current_key = cfg.get("openrouter_api_key", "")
    masked_key = (current_key[:6] + "..." + current_key[-4:]) if len(current_key) > 10 else ("Configured" if current_key else "Not Set")

    console.print("\n[bold cyan]OPENROUTER AI CONFIGURATION[/bold cyan]")
    console.print(f"API Key: [bold]{masked_key}[/bold]")
    console.print(f"Active Model: [bold green]{cfg.get('openrouter_model')}[/bold green]")
    console.print(f"Language: [bold yellow]{cfg.get('language').upper()}[/bold yellow]")
    console.print("")
    console.print("[1] Set OpenRouter API Key")
    console.print("[2] Select AI Model")
    console.print("[3] Test API Connection")
    console.print("[0] Back")

    choice = input("sunscan/ai > ").strip()
    if choice == "1":
        new_key = input("Enter OpenRouter API Key: ").strip()
        if new_key:
            set_config_value("openrouter_api_key", new_key)
            console.print("[green]API Key saved securely in local config.[/green]\n")
    elif choice == "2":
        console.print("\nAvailable Models:")
        for idx, m in enumerate(POPULAR_MODELS, start=1):
            console.print(f"[{idx}] {m['name']} ({m['id']})")
        m_choice = input("Select model number: ").strip()
        try:
            m_idx = int(m_choice) - 1
            if 0 <= m_idx < len(POPULAR_MODELS):
                set_config_value("openrouter_model", POPULAR_MODELS[m_idx]["id"])
                console.print(f"[green]Model updated to {POPULAR_MODELS[m_idx]['id']}![/green]\n")
        except ValueError:
            pass
    elif choice == "3":
        client = OpenRouterClient()
        success, msg = client.test_connection()
        if success:
            console.print(f"[bold green]SUCCESS:[/bold green] {msg}\n")
        else:
            console.print(f"[bold red]FAILED:[/bold red] {msg}\n")


def _handle_diagnostics(lang: str):
    console.print("\n[bold cyan]SYSTEM DIAGNOSTICS & TELEMETRY[/bold cyan]")
    env = detect_platform_details()
    table = Table(show_header=False)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Operating System", env.get("system", ""))
    table.add_row("Distribution", env.get("distro", ""))
    table.add_row("Architecture", env.get("machine", ""))
    table.add_row("Python Version", env.get("python_version", ""))
    table.add_row("Package Manager", env.get("package_manager") or "None detected")
    table.add_row("Root / Elevated", str(env.get("is_root", False)))
    table.add_row("Termux Environment", str(env.get("is_termux", False)))

    console.print(table)
    console.print("")
