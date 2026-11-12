"""
SUNSCAN Input & Target Validator
Organization: CodeSun
License: MIT
"""

import ipaddress
import re
from typing import Tuple, Optional
from urllib.parse import urlparse

# Strict regex patterns for hostnames and domains
HOSTNAME_REGEX = re.compile(
    r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
)
UNSAFE_CHARS_REGEX = re.compile(r"[;&|`$><!\\'\"]")


def is_valid_ipv4(target: str) -> bool:
    try:
        ip = ipaddress.IPv4Address(target.strip())
        return True
    except ValueError:
        return False


def is_valid_ipv6(target: str) -> bool:
    try:
        ip = ipaddress.IPv6Address(target.strip())
        return True
    except ValueError:
        return False


def is_valid_cidr(target: str) -> bool:
    try:
        network = ipaddress.ip_network(target.strip(), strict=False)
        return True
    except ValueError:
        return False


def is_valid_hostname(target: str) -> bool:
    target = target.strip()
    if len(target) > 253 or len(target) == 0:
        return False
    return bool(HOSTNAME_REGEX.match(target))


def is_valid_url(target: str) -> bool:
    target = target.strip()
    try:
        parsed = urlparse(target)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        return is_valid_hostname(hostname) or is_valid_ipv4(hostname) or is_valid_ipv6(hostname)
    except Exception:
        return False


def contains_unsafe_shell_characters(value: str) -> bool:
    """Checks for characters that might attempt shell escaping or injection."""
    return bool(UNSAFE_CHARS_REGEX.search(value))


def validate_target(target: str) -> Tuple[bool, str, str]:
    """
    Validates a target input.
    Returns: (is_valid, target_type, normalized_value_or_error_message)
    """
    cleaned = target.strip()
    if not cleaned:
        return False, "empty", "Target cannot be empty."

    if contains_unsafe_shell_characters(cleaned):
        return False, "unsafe", "Target contains disallowed shell characters."

    # Check if URL
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        if is_valid_url(cleaned):
            return True, "url", cleaned
        return False, "invalid_url", "Invalid URL format."

    # Check if CIDR
    if "/" in cleaned:
        if is_valid_cidr(cleaned):
            return True, "cidr", cleaned
        return False, "invalid_cidr", "Invalid CIDR range."

    # Check IPv4
    if is_valid_ipv4(cleaned):
        return True, "ipv4", cleaned

    # Check IPv6
    if is_valid_ipv6(cleaned):
        return True, "ipv6", cleaned

    # Check Hostname / Domain
    if is_valid_hostname(cleaned):
        return True, "domain", cleaned

    # Allow simple username alphanumeric target for OSINT (sherlock)
    if re.match(r"^[a-zA-Z0-9_\-\.]{1,64}$", cleaned):
        return True, "handle", cleaned

    return False, "unknown", f"Unrecognized target format: '{cleaned}'"


def normalize_target_for_tool(target: str, expected_type: str = "host") -> str:
    """Normalizes target string (e.g. extracts hostname from URL if tool expects hostname)."""
    cleaned = target.strip()
    if expected_type == "url":
        if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
            return f"http://{cleaned}"
        return cleaned
    elif expected_type in ("host", "ip", "domain"):
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            parsed = urlparse(cleaned)
            return parsed.hostname or cleaned
    return cleaned
