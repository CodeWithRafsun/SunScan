"""
SUNSCAN Unified Scan Output Analyzer
Organization: CodeSun
License: MIT
"""

import re
from typing import Dict, Any, List, Optional
from ai.openrouter import OpenRouterClient
from engine.config import get_config_value


def analyze_heuristically(tool_name: str, target: str, raw_output: str, language: str = "en") -> Dict[str, Any]:
    """
    Offline heuristic analyzer providing structured security insights without external AI calls.
    Extracts open ports, services, headers, and obvious error/vulnerability banners.
    """
    findings: List[Dict[str, Any]] = []
    lines = raw_output.splitlines()

    # Rule 1: Detect open ports from Nmap/Masscan output
    open_port_regex = re.compile(r"^(\d+/(?:tcp|udp))\s+open\s+(\S+)\s*(.*)$")
    for line in lines:
        match = open_port_regex.match(line.strip())
        if match:
            port_proto = match.group(1)
            service = match.group(2)
            version = match.group(3).strip()
            title = f"Open Port Exposed: {port_proto} ({service})" if language == "en" else f"উন্মুক্ত পোর্ট শনাক্ত: {port_proto} ({service})"
            explanation = (
                f"Service '{service}' is listening and accepting connections on {port_proto}. {f'Version detected: {version}' if version else ''}"
                if language == "en"
                else f"পোর্ট {port_proto} এ '{service}' সার্ভিসটি সচল ও কানেকশন গ্রহণ করছে। {f'ভার্সন: {version}' if version else ''}"
            )
            recom = (
                "Ensure firewall rules restrict access only to authorized subnets, and keep the service software updated."
                if language == "en"
                else "ফায়ারওয়াল রুল যাচাই করে অননুমোদিত অ্যাক্সেস ব্লক করুন এবং সার্ভিসের সর্বশেষ সিকিউরিটি প্যাচ নিশ্চিত করুন।"
            )
            findings.append({
                "title": title,
                "severity": "low" if port_proto.startswith("80/") or port_proto.startswith("443/") else "medium",
                "confidence": "high",
                "evidence": line.strip(),
                "explanation": explanation,
                "impact": "Unrestricted exposed services increase the perimeter attack surface." if language == "en" else "উন্মুক্ত পোর্ট সার্ভারের আক্রমণ ক্ষেত্র বাড়িয়ে দেয়।",
                "recommendation": recom,
            })

    # Rule 2: Insecure HTTP methods / missing security headers in Nikto / WhatWeb
    for line in lines:
        lower = line.lower()
        if "anti-clickjacking" in lower or "x-frame-options" in lower:
            findings.append({
                "title": "Missing X-Frame-Options Header" if language == "en" else "X-Frame-Options হেডার অনুপস্থিত",
                "severity": "low",
                "confidence": "high",
                "evidence": line.strip(),
                "explanation": "The web server does not provide an anti-clickjacking header." if language == "en" else "ওয়েব সার্ভার ক্লিকজ্যাকিং প্রতিরোধের হেডার পাঠায়নি।",
                "impact": "The site could be embedded in malicious iframes to deceive users." if language == "en" else "ক্ষতিকর সাইটে আইফ্রেমের মাধ্যমে ক্লিকজ্যাকিং হামলার ঝুঁকি থাকে।",
                "recommendation": "Configure 'X-Frame-Options: SAMEORIGIN' or Content-Security-Policy." if language == "en" else "ওয়েব সার্ভারে 'X-Frame-Options: SAMEORIGIN' কনফিগার করুন।",
            })
        elif "vulnerable" in lower or "cve-" in lower:
            match_cve = re.search(r"CVE-\d{4}-\d+", line, re.IGNORECASE)
            cve_str = match_cve.group(0) if match_cve else "Vulnerability Mention"
            findings.append({
                "title": f"Potential Vulnerability Identified: {cve_str}" if language == "en" else f"সম্ভাব্য সিকিউরিটি ত্রুটি: {cve_str}",
                "severity": "high",
                "confidence": "medium",
                "evidence": line.strip(),
                "explanation": f"Scanner highlighted a potential security issue: {line.strip()}" if language == "en" else f"স্ক্যানারে সম্ভাব্য সিকিউরিটি দুর্বলতার সংকেত পাওয়া গেছে: {line.strip()}",
                "impact": "Known CVEs can allow unauthorized access if not patched." if language == "en" else "অনিরাপদ কোড বা ভার্সনে সিস্টেম অ্যাক্সেসের ঝুঁকি তৈরি হতে পারে।",
                "recommendation": "Review security advisories for the identified software version and patch immediately." if language == "en" else "সংশ্লিষ্ট সফটওয়্যারের অফিসিয়াল প্যাচ বা আপডেট ইন্সটল করুন।",
            })

    summary_text = (
        f"Completed automated analysis for {tool_name} against target {target}. Found {len(findings)} noteworthy security items."
        if language == "en"
        else f"{target} টার্গেটে {tool_name} স্ক্যানের অফলাইন বিশ্লেষণ সম্পন্ন। মোট {len(findings)}টি পর্যবেক্ষণ পাওয়া গেছে।"
    )

    return {
        "summary": summary_text,
        "risk_score": "high" if any(f["severity"] == "high" for f in findings) else ("medium" if findings else "low"),
        "findings": findings,
        "limitations": [
            "Heuristic analysis does not use external LLM reasoning; results are derived from pattern matching."
            if language == "en"
            else "হিউরিস্টিক বিশ্লেষণে বাহ্যিক এআই মডেল ব্যবহৃত হয়নি, প্যাটার্ন ম্যাচিংয়ের মাধ্যমে ফলাফল তৈরি হয়েছে।"
        ],
        "next_steps": [
            "Conduct manual verification of highlighted ports and headers."
            if language == "en"
            else "শনাক্তকৃত পোর্ট ও হেডারগুলো নিজে যাচাই করুন।"
        ],
    }


def analyze_scan(
    tool_name: str,
    target: str,
    raw_output: str,
    use_ai: bool = True,
    language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main dispatch function: uses OpenRouter AI if configured and requested,
    otherwise falls back gracefully to offline heuristic analysis.
    """
    selected_lang = language or get_config_value("language", "en")

    if use_ai:
        api_key = get_config_value("openrouter_api_key", "")
        if api_key:
            client = OpenRouterClient(api_key=api_key)
            success, ai_result, error = client.analyze_scan_output(
                tool_name=tool_name,
                target=target,
                raw_output=raw_output,
                language=selected_lang,
            )
            if success and ai_result:
                return ai_result

    # Fallback to local heuristic analysis
    return analyze_heuristically(tool_name, target, raw_output, selected_lang)
