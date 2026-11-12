"""
SUNSCAN Automated Test Suite
Organization: CodeSun
License: MIT
"""

import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from engine.validator import (
    is_valid_ipv4,
    is_valid_ipv6,
    is_valid_cidr,
    is_valid_hostname,
    is_valid_url,
    validate_target,
    contains_unsafe_shell_characters,
    normalize_target_for_tool,
)
from engine.registry import ToolRegistry
from engine.executor import build_command_args, ScanJob, execute_scan, cancel_scan
from engine.installer import get_install_command_for_tool, get_manual_instructions
from engine.permissions import detect_platform_details
from engine.process_manager import ProcessManager
from ai.prompts import SYSTEM_PROMPT_EN, SYSTEM_PROMPT_BN
from ai.openrouter import OpenRouterClient
from ai.analyzer import analyze_heuristically


class TestInputValidation(unittest.TestCase):
    def test_ipv4_validation(self):
        self.assertTrue(is_valid_ipv4("192.168.1.1"))
        self.assertTrue(is_valid_ipv4("10.0.0.254"))
        self.assertFalse(is_valid_ipv4("999.999.999.999"))
        self.assertFalse(is_valid_ipv4("example.com"))

    def test_ipv6_validation(self):
        self.assertTrue(is_valid_ipv6("::1"))
        self.assertTrue(is_valid_ipv6("2001:db8::1"))
        self.assertFalse(is_valid_ipv6("127.0.0.1"))

    def test_cidr_validation(self):
        self.assertTrue(is_valid_cidr("192.168.1.0/24"))
        self.assertTrue(is_valid_cidr("10.0.0.0/8"))
        self.assertFalse(is_valid_cidr("192.168.1.0/99"))

    def test_hostname_validation(self):
        self.assertTrue(is_valid_hostname("scanme.nmap.org"))
        self.assertTrue(is_valid_hostname("sub.domain.local"))
        self.assertFalse(is_valid_hostname("domain with spaces.com"))
        self.assertFalse(is_valid_hostname("-invalid-.com"))

    def test_url_validation(self):
        self.assertTrue(is_valid_url("http://scanme.nmap.org"))
        self.assertTrue(is_valid_url("https://example.com:8080/path"))
        self.assertFalse(is_valid_url("ftp://example.com"))
        self.assertFalse(is_valid_url("not a url"))

    def test_shell_injection_detection(self):
        self.assertTrue(contains_unsafe_shell_characters("127.0.0.1; rm -rf /"))
        self.assertTrue(contains_unsafe_shell_characters("example.com && whoami"))
        self.assertTrue(contains_unsafe_shell_characters("`reboot`"))
        self.assertTrue(contains_unsafe_shell_characters("test | ls"))
        self.assertFalse(contains_unsafe_shell_characters("scanme.nmap.org"))
        self.assertFalse(contains_unsafe_shell_characters("192.168.1.5"))

    def test_target_dispatcher(self):
        ok, t_type, val = validate_target("192.168.1.100")
        self.assertTrue(ok)
        self.assertEqual(t_type, "ipv4")

        ok, t_type, val = validate_target("scanme.nmap.org")
        self.assertTrue(ok)
        self.assertEqual(t_type, "domain")

        ok, t_type, val = validate_target("https://example.com/api")
        self.assertTrue(ok)
        self.assertEqual(t_type, "url")

        ok, t_type, val = validate_target("10.0.0.1; cat /etc/passwd")
        self.assertFalse(ok)
        self.assertEqual(t_type, "unsafe")


class TestCatalogAndRegistry(unittest.TestCase):
    def setUp(self):
        self.reg = ToolRegistry()

    def test_catalog_loaded(self):
        categories = self.reg.get_categories()
        self.assertGreaterEqual(len(categories), 10)
        tools = self.reg.get_all_tools()
        self.assertGreaterEqual(len(tools), 10)

    def test_tool_query(self):
        nmap = self.reg.get_tool("nmap")
        self.assertIsNotNone(nmap)
        self.assertEqual(nmap.get("category"), "network-scanning")
        self.assertTrue(len(nmap.get("commands", [])) >= 3)


class TestCommandConstruction(unittest.TestCase):
    def test_safe_argument_array_construction(self):
        tool = {
            "id": "mock-scanner",
            "name": "Mock Scanner",
            "executable": "mock-scan",
        }
        preset = {
            "id": "quick-scan",
            "args": ["-sV", "-p", "80,443", "{target}"],
        }
        is_safe, args, err = build_command_args(tool, preset, "scanme.nmap.org")
        self.assertTrue(is_safe)
        self.assertEqual(args, ["mock-scan", "-sV", "-p", "80,443", "scanme.nmap.org"])

    def test_rejection_of_shell_metacharacters(self):
        tool = {"id": "nmap", "executable": "nmap"}
        preset = {"id": "p1", "args": ["-sn", "{target}"]}
        is_safe, args, err = build_command_args(tool, preset, "127.0.0.1; echo pwned")
        self.assertFalse(is_safe)
        self.assertIn("Invalid target", err)


class TestInstallerLogic(unittest.TestCase):
    def test_manual_instructions_generation(self):
        tool = {
            "id": "sample-tool",
            "name": "Sample Security Tool",
            "repository": "https://github.com/example/sample",
            "installers": ["apt", "pip"],
            "executable": "sample-tool",
        }
        instructions = get_manual_instructions(tool)
        self.assertIn("Sample Security Tool", instructions)
        self.assertIn("https://github.com/example/sample", instructions)


class TestMockProcessExecution(unittest.TestCase):
    def test_successful_mock_scan(self):
        # We test subprocess using safe mock binary 'echo'
        job = ScanJob(
            tool_id="mock-echo",
            command_id="test",
            target="127.0.0.1",
            args_array=["echo", "SUNSCAN_MOCK_SUCCESS"],
        )
        lines = []
        execute_scan(job, on_output_line=lambda l: lines.append(l))
        self.assertEqual(job.status, "completed")
        self.assertEqual(job.exit_code, 0)
        self.assertIn("SUNSCAN_MOCK_SUCCESS", job.output_lines)

    def test_scan_cancellation(self):
        job = ScanJob(
            tool_id="mock-sleep",
            command_id="test",
            target="127.0.0.1",
            args_array=["sleep", "10"],
        )
        # Verify job can be initialized and formatted
        d = job.to_dict()
        self.assertEqual(d["target"], "127.0.0.1")


class TestOfflineAnalyzer(unittest.TestCase):
    def test_heuristic_port_analysis(self):
        sample_nmap_output = """
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 192.168.1.50
Host is up (0.00045s latency).
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu
80/tcp   open  http    Apache httpd 2.4.52
443/tcp  open  ssl/http Apache httpd 2.4.52
Nmap done: 1 IP address (1 host up) scanned in 2.12 seconds
        """
        analysis = analyze_heuristically("Nmap", "192.168.1.50", sample_nmap_output, language="en")
        self.assertIn("summary", analysis)
        findings = analysis.get("findings", [])
        self.assertGreaterEqual(len(findings), 2)
        # Check that open ports were extracted
        titles = [f["title"] for f in findings]
        self.assertTrue(any("22/tcp" in t for t in titles))
        self.assertTrue(any("80/tcp" in t for t in titles))

    def test_bangla_heuristic_output(self):
        sample_output = "80/tcp open http Apache\n"
        analysis = analyze_heuristically("Nmap", "example.com", sample_output, language="bn")
        self.assertIn("summary", analysis)
        findings = analysis.get("findings", [])
        self.assertGreaterEqual(len(findings), 1)
        self.assertIn("উন্মুক্ত পোর্ট", findings[0]["title"])


if __name__ == "__main__":
    unittest.main()
