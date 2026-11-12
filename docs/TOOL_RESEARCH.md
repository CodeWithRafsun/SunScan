# SUNSCAN Tool Research Document (PHASE 1)
**Project:** SUNSCAN (Modular Cybersecurity Toolkit & AI-Powered Output Analyzer)  
**Organization:** CodeSun  
**License:** MIT  
**Version:** 1.0.0-research  
**Classification:** Defensive Cybersecurity Tool Catalog & Authorized Audit Reference

---

## Executive Summary
This document provides empirical research, architectural telemetry, and integration feasibility analysis for verified open-source and standard cybersecurity utilities across 10 mandatory and 10 extended categories. Each tool has been validated against official source repositories, package registries (Debian/Ubuntu `apt`, Termux `pkg`, Arch `pacman`, Fedora `dnf`, Homebrew, GitHub releases), runtime dependencies, structured output capabilities (JSON, XML, CSV), and safe CLI execution parameters.

SUNSCAN enforces strict non-invasive defaults, zero automatic bulk installations, explicit user confirmation for target authorization, and POSIX/subprocess safe isolation without `shell=True`.

---

## Category 1: Network Scanning

### 1. Nmap (Network Mapper)
- **Official URL:** https://nmap.org/
- **Repository:** https://github.com/nmap/nmap
- **Primary Purpose:** Network discovery, port scanning, OS and service version detection.
- **Maintenance Status:** Actively maintained (v7.95+).
- **Supported OS:** Linux (Debian, Ubuntu, Kali, Arch, Fedora), macOS, Windows, Termux (rootless TCP connect mode, full raw sockets with root/chroot).
- **Installation Methods:** `apt-get install nmap`, `pkg install nmap`, `pacman -S nmap`, `dnf install nmap`, source build.
- **Runtime Dependencies:** `libpcap`, `libpcre`, `openssl`, `lua` (for NSE engine).
- **CLI Functionality:** Yes (`nmap [Scan Type...] [Options] {target specification}`).
- **Structured Output:** Yes (`-oX` XML, `-oJ` via community wrappers, `-oG` grepable, `-oN` normal).
- **Integration Feasibility:** High. Standard defensive tool for perimeter inventory.

### 2. Masscan
- **Official URL:** https://github.com/robertdavidgraham/masscan
- **Repository:** https://github.com/robertdavidgraham/masscan
- **Primary Purpose:** High-speed asynchronous TCP port scanner capable of scanning entire CIDRs.
- **Maintenance Status:** Maintained by community and Robert Graham.
- **Supported OS:** Linux (Debian, Ubuntu, Kali), macOS. Termux requires root/proot for raw packet driver.
- **Installation Methods:** `apt-get install masscan`, build from source (`make`).
- **Runtime Dependencies:** `libpcap-dev`, Linux raw socket capabilities (`CAP_NET_RAW`).
- **CLI Functionality:** Yes (`masscan -p<ports> <ip/range> --rate=<pps>`).
- **Structured Output:** Yes (`-oJ` JSON, `-oX` XML, `-oB` binary).
- **Integration Feasibility:** Medium-High. Rate-limiting safeguards mandatory in SUNSCAN presets.

### 3. RustScan
- **Official URL:** https://rustscan.github.io/RustScan/
- **Repository:** https://github.com/RustScan/RustScan
- **Primary Purpose:** Modern fast port scanner written in Rust that pipes open ports to Nmap.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Docker, Termux (via `cargo` or precompiled musl binaries).
- **Installation Methods:** `cargo install rustscan`, `.deb` release, Homebrew, Docker.
- **Runtime Dependencies:** Rust runtime (static binary), optional Nmap for second-stage interrogation.
- **CLI Functionality:** Yes (`rustscan -a <target> -- <nmap-flags>`).
- **Structured Output:** Yes (supports `-g` greppable and `--accessible` clean JSON output).
- **Integration Feasibility:** High. Safe, fast, non-intrusive port identification.

### 4. ARP-scan
- **Official URL:** https://github.com/royhills/arp-scan
- **Repository:** https://github.com/royhills/arp-scan
- **Primary Purpose:** ARP packet scanner to discover active IPv4 hosts on local Ethernet/Wi-Fi subnets.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install arp-scan`, `pacman -S arp-scan`, source build.
- **Runtime Dependencies:** `libpcap`, raw network device access.
- **CLI Functionality:** Yes (`arp-scan --localnet`, `arp-scan -I <interface> <target>`).
- **Structured Output:** Text, plain delimited format with `-x` / `--plain`.
- **Integration Feasibility:** High for local network diagnostic and inventory.

### 5. Netdiscover
- **Official URL:** https://github.com/alexxy/netdiscover
- **Repository:** https://github.com/alexxy/netdiscover
- **Primary Purpose:** Active/passive ARP reconnaissance tool for wireless and switched LAN networks.
- **Maintenance Status:** Maintained in Debian/Kali packages.
- **Supported OS:** Linux, BSD.
- **Installation Methods:** `apt-get install netdiscover`.
- **Runtime Dependencies:** `libpcap`, `libnet`.
- **CLI Functionality:** Yes (`netdiscover -r <cidr> -P`).
- **Structured Output:** Plain text, tabular formatting.
- **Integration Feasibility:** Medium. Best used in passive `-p` or single-burst `-r` mode.

### 6. Angry IP Scanner (ipscan)
- **Official URL:** https://angryip.org/
- **Repository:** https://github.com/angryip/ipscan
- **Primary Purpose:** Multi-threaded IP address and port scanner.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, Windows, macOS (CLI and GUI modes).
- **Installation Methods:** `.deb`, `.rpm`, Homebrew, standalone `.jar`.
- **Runtime Dependencies:** OpenJDK / JRE >= 11.
- **CLI Functionality:** Yes (`ipscan -s -f:csv <range> -o <file>`).
- **Structured Output:** CSV, TXT, XML.
- **Integration Feasibility:** Medium. Requires Java runtime on host.

### 7. ZMap
- **Official URL:** https://zmap.io/
- **Repository:** https://github.com/zmap/zmap
- **Primary Purpose:** Fast single-packet network scanner for Internet-wide network surveys.
- **Maintenance Status:** Maintained by Stanford / University of Michigan researchers.
- **Supported OS:** Linux (Debian, Ubuntu, Fedora), macOS.
- **Installation Methods:** `apt-get install zmap`, `pacman -S zmap`, source build (`cmake`).
- **Runtime Dependencies:** `libpcap`, `libgmp`, `libjson-c`.
- **CLI Functionality:** Yes (`zmap -p 443 <cidr> -o output.csv`).
- **Structured Output:** CSV, JSON output module (`--output-module=json`).
- **Integration Feasibility:** High. Strict authorization safeguards required.

### 8. Naabu
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/naabu
- **Primary Purpose:** Fast Go-based port scanner focusing on simplicity and pipeline integration.
- **Maintenance Status:** Actively maintained by ProjectDiscovery.
- **Supported OS:** Linux, macOS, Windows, Termux (via `go install`).
- **Installation Methods:** `pdtm -i naabu`, `go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest`, GitHub release binaries.
- **Runtime Dependencies:** Go standalone binary or `libpcap` for SYN stealth scans (connect scan works rootless).
- **CLI Functionality:** Yes (`naabu -host <target> -json`).
- **Structured Output:** Native JSON lines (`-json`).
- **Integration Feasibility:** Very High. Excellent JSON streaming support for AI analysis.

### 9. Unicornscan
- **Official URL:** http://www.unicornscan.org/ / Debian package tracking
- **Repository:** https://gitlab.com/kalilinux/packages/unicornscan
- **Primary Purpose:** Asynchronous TCP and UDP port scanner with stimulus/response engine.
- **Maintenance Status:** Legacy / maintenance mode in Kali Linux.
- **Supported OS:** Linux (Kali, Debian).
- **Installation Methods:** `apt-get install unicornscan`.
- **Runtime Dependencies:** `libpcap`, `libdnet`.
- **CLI Functionality:** Yes (`unicornscan -mT <target>:1-1024`).
- **Structured Output:** Plain text, database output backend.
- **Integration Feasibility:** Medium. Handled as optional legacy utility.

### 10. Hping3
- **Official URL:** http://www.hping.org/
- **Repository:** https://github.com/antirez/hping
- **Primary Purpose:** Command-line oriented TCP/IP packet assembler and network auditing analyzer.
- **Maintenance Status:** Maintained in Debian/Ubuntu repos.
- **Supported OS:** Linux, BSD, macOS.
- **Installation Methods:** `apt-get install hping3`, `pacman -S hping`.
- **Runtime Dependencies:** `libpcap`, `tcl`.
- **CLI Functionality:** Yes (`hping3 -S -p 80 -c 4 <target>`).
- **Structured Output:** Custom stdout stream.
- **Integration Feasibility:** Medium. Requires root privileges for raw socket transmission.

---

## Category 2: Web Security Scanning

### 1. Nikto
- **Official URL:** https://cirt.net/Nikto2
- **Repository:** https://github.com/sullo/nikto
- **Primary Purpose:** Open source web server scanner for outdated software, misconfigurations, default files.
- **Maintenance Status:** Actively maintained (v2.5.0+).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install nikto`, `git clone` (Perl script), Docker.
- **Runtime Dependencies:** Perl 5, `Net::SSLeay`.
- **CLI Functionality:** Yes (`nikto -h <target> -Format json -o <file>`).
- **Structured Output:** JSON (`-Format json`), XML, CSV, HTML, TXT.
- **Integration Feasibility:** Very High. Clean structured JSON output parsing.

### 2. WhatWeb
- **Official URL:** https://morningstarsecurity.com/research/whatweb
- **Repository:** https://github.com/urbanadventurer/WhatWeb
- **Primary Purpose:** Next generation web scanner identifying CMS, blogging platforms, JavaScript libraries, and server technologies.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `apt-get install whatweb`, `gem install whatweb`, `git clone`.
- **Runtime Dependencies:** Ruby >= 2.5.
- **CLI Functionality:** Yes (`whatweb <target> --log-json=<file>`).
- **Structured Output:** Native JSON (`--log-json=<file>`), XML, Brief text.
- **Integration Feasibility:** Very High. Extremely benign, passive/polite fingerprinting with perfect JSON.

### 3. Wapiti
- **Official URL:** https://wapiti-scanner.github.io/
- **Repository:** https://github.com/wapiti-scanner/wapiti
- **Primary Purpose:** Black-box web application vulnerability auditor (XSS, SQLi, SSRF, open redirects).
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pip install wapiti3`, `apt-get install wapiti`.
- **Runtime Dependencies:** Python 3, `requests`, `beautifulsoup4`, `tld`.
- **CLI Functionality:** Yes (`wapiti -u <url> -f json -o report.json`).
- **Structured Output:** JSON (`-f json`), HTML, XML.
- **Integration Feasibility:** High. Modular Python architecture.

### 4. OWASP ZAP (ZAP CLI / Automation Framework)
- **Official URL:** https://www.zaproxy.org/
- **Repository:** https://github.com/zaproxy/zaproxy
- **Primary Purpose:** Full-featured dynamic application security testing (DAST) proxy and scanner.
- **Maintenance Status:** Actively maintained by OWASP/Checkmarx community.
- **Supported OS:** Linux, macOS, Windows, Docker.
- **Installation Methods:** `apt-get install zaproxy`, Snap, Docker container, Zap-CLI wrapper (`pip install zapcli`).
- **Runtime Dependencies:** Java JRE >= 17.
- **CLI Functionality:** Yes (`zap.sh -cmd -quickurl <target> -quickout report.json`).
- **Structured Output:** JSON, XML, HTML, Markdown.
- **Integration Feasibility:** High (via headless automation framework or docker integration).

### 5. Nuclei
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/nuclei
- **Primary Purpose:** Fast and customizable vulnerability scanner based on community YAML templates.
- **Maintenance Status:** Actively maintained by ProjectDiscovery.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`, `brew install nuclei`, GitHub binary releases.
- **Runtime Dependencies:** Go static binary.
- **CLI Functionality:** Yes (`nuclei -u <target> -j -o results.json`).
- **Structured Output:** Native JSON Lines (`-jsonl` / `-j`).
- **Integration Feasibility:** Exceptional. Clean standardized JSON output with CVE references.

### 6. Skipfish
- **Official URL:** https://code.google.com/archive/p/skipfish/
- **Repository:** https://gitlab.com/kalilinux/packages/skipfish
- **Primary Purpose:** High-performance web application security reconnaissance tool.
- **Maintenance Status:** Archived / legacy maintenance in Debian.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `apt-get install skipfish`.
- **Runtime Dependencies:** `libidn`, `libpcre`, `openssl`.
- **CLI Functionality:** Yes (`skipfish -o <dir> <url>`).
- **Structured Output:** Interactive HTML/JS report bundle.
- **Integration Feasibility:** Medium. Useful for deep recursive heuristic crawl auditing.

### 7. Arachni
- **Official URL:** https://www.arachni-scanner.com/
- **Repository:** https://github.com/Arachni/arachni
- **Primary Purpose:** Modular, high-performance Ruby-based web vulnerability framework.
- **Maintenance Status:** Community archival; portable packages available.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** Self-contained tarball / Docker.
- **Runtime Dependencies:** Bundled Ruby runtime.
- **CLI Functionality:** Yes (`arachni --report-save-path=report.afr <url>`).
- **Structured Output:** AFR (Arachni Framework Report) exportable to JSON, XML, HTML.
- **Integration Feasibility:** Medium. Large standalone footprint.

### 8. W3af
- **Official URL:** http://w3af.org/
- **Repository:** https://github.com/andresriancho/w3af
- **Primary Purpose:** Web application attack and audit framework.
- **Maintenance Status:** Legacy Python 2.x codebase; Docker is required for modern execution.
- **Supported OS:** Linux (via Docker/py2 legacy).
- **Installation Methods:** Docker (`docker pull andresriancho/w3af`).
- **Runtime Dependencies:** Python 2.7 (legacy), pip packages.
- **CLI Functionality:** Yes (`w3af_console -s script.w3af`).
- **Structured Output:** XML, CSV, HTML.
- **Integration Feasibility:** Low-Medium. SUNSCAN flags legacy status and recommends Nuclei/Wapiti alternatives.

### 9. Webanalyze
- **Official URL:** https://github.com/rverton/webanalyze
- **Repository:** https://github.com/rverton/webanalyze
- **Primary Purpose:** Port of Wappalyzer to Go for ultra-fast web tech identification.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install github.com/rverton/webanalyze/cmd/webanalyze@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`webanalyze -host <target> -output json`).
- **Structured Output:** Native JSON.
- **Integration Feasibility:** High. Fast, zero-risk fingerprinting.

### 10. SSLyze
- **Official URL:** https://github.com/nabla-c0d3/sslyze
- **Repository:** https://github.com/nabla-c0d3/sslyze
- **Primary Purpose:** Fast and comprehensive TLS/SSL configuration scanner and certificate auditor.
- **Maintenance Status:** Actively maintained (Python 3.10+).
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pip install sslyze`, `apt-get install sslyze`.
- **Runtime Dependencies:** Python 3, `cryptography`, `tls-parser`.
- **CLI Functionality:** Yes (`sslyze --json_out=report.json <target>`).
- **Structured Output:** Native JSON schema (`--json_out`).
- **Integration Feasibility:** Exceptional. Industry standard for TLS compliance verification.

---

## Category 3: SQL Injection Testing & Database Auditing

### 1. SQLMap
- **Official URL:** https://sqlmap.org/
- **Repository:** https://github.com/sqlmapproject/sqlmap
- **Primary Purpose:** Automatic SQL injection and database takeover auditing tool.
- **Maintenance Status:** Actively maintained (daily updates).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install sqlmap`, `pkg install sqlmap`, `pip install sqlmap`, `git clone`.
- **Runtime Dependencies:** Python 3 standard library.
- **CLI Functionality:** Yes (`sqlmap -u "<target>" --batch --risk=1 --level=1`).
- **Structured Output:** Text, SQLite session database, XML/CSV dumping.
- **Integration Feasibility:** High. SUNSCAN restricts default presets to benign `--level=1 --risk=1` verification.

### 2. Ghauri
- **Official URL:** https://github.com/r0oth3x49/ghauri
- **Repository:** https://github.com/r0oth3x49/ghauri
- **Primary Purpose:** Lightweight, cross-platform Python tool for detecting and auditing SQL injection flaws.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `pip install ghauri`.
- **Runtime Dependencies:** Python 3, `requests`, `colorama`.
- **CLI Functionality:** Yes (`ghauri -u "<url>" --batch`).
- **Structured Output:** Plain text log.
- **Integration Feasibility:** High. Clean Python CLI.

### 3. jSQL Injection
- **Official URL:** https://github.com/ron190/jsql-injection
- **Repository:** https://github.com/ron190/jsql-injection
- **Primary Purpose:** Java application for automatic SQL injection detection and database interrogation.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install jsql`, `.jar` executable download.
- **Runtime Dependencies:** Java JRE >= 11.
- **CLI Functionality:** Yes (`java -jar jsql-injection.jar -cli -url <url>`).
- **Structured Output:** Console text, XML logs.
- **Integration Feasibility:** Medium. Requires JRE.

### 4. NoSQLMap
- **Official URL:** https://github.com/codingo/NoSQLMap
- **Repository:** https://github.com/codingo/NoSQLMap
- **Primary Purpose:** Automated auditing tool for MongoDB, CouchDB, and NoSQL injection vulnerabilities.
- **Maintenance Status:** Maintained by community.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `pip install nosqlmap`, `git clone`.
- **Runtime Dependencies:** Python 3, `pymongo`, `requests`.
- **CLI Functionality:** Yes (`nosqlmap --cli`).
- **Structured Output:** Text logs.
- **Integration Feasibility:** High for modern NoSQL API audits.

### 5. DSSS (Damn Small SQLi Scanner)
- **Official URL:** https://github.com/stamparm/DSSS
- **Repository:** https://github.com/stamparm/DSSS
- **Primary Purpose:** Minimalist (under 100 lines) fully functional SQL injection vulnerability scanner.
- **Maintenance Status:** Maintained by Miroslav Stampar (sqlmap co-author).
- **Supported OS:** All OS running Python.
- **Installation Methods:** Direct download / git clone.
- **Runtime Dependencies:** Python 3 standard library (`urllib`).
- **CLI Functionality:** Yes (`python3 dsss.py -u "<url>"`).
- **Structured Output:** Plain text.
- **Integration Feasibility:** High. Zero third-party dependencies, safe for containerized tests.

### 6. BBQSQL
- **Official URL:** https://github.com/infobyte/bbqsql
- **Repository:** https://github.com/infobyte/bbqsql
- **Primary Purpose:** Blind SQL injection auditing framework.
- **Maintenance Status:** Legacy / archival.
- **Supported OS:** Linux (Python 2/3 compatibility forks).
- **Installation Methods:** `pip install bbqsql`.
- **Runtime Dependencies:** Python, gevent.
- **CLI Functionality:** Yes (`bbqsql`).
- **Structured Output:** Text, exportable logs.
- **Integration Feasibility:** Low-Medium. Flagged as legacy reference.

### 7. Blisqy
- **Official URL:** https://github.com/JohnTroony/Blisqy
- **Repository:** https://github.com/JohnTroony/Blisqy
- **Primary Purpose:** Time-based blind SQL injection audit tool specializing in HTTP header injection.
- **Maintenance Status:** Maintained on GitHub.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `git clone https://github.com/JohnTroony/Blisqy`.
- **Runtime Dependencies:** Python 3, `requests`.
- **CLI Functionality:** Yes (`python3 blisqy.py`).
- **Structured Output:** Text.
- **Integration Feasibility:** Medium. Specialized test cases.

### 8. SQLNinja
- **Official URL:** http://sqlninja.sourceforge.net/
- **Repository:** https://gitlab.com/kalilinux/packages/sqlninja
- **Primary Purpose:** Targeted Microsoft SQL Server vulnerability audit tool.
- **Maintenance Status:** Legacy maintenance in Debian/Kali.
- **Supported OS:** Linux.
- **Installation Methods:** `apt-get install sqlninja`.
- **Runtime Dependencies:** Perl, Net::Pcap.
- **CLI Functionality:** Yes (`sqlninja -m <mode> -f <config>`).
- **Structured Output:** Console text.
- **Integration Feasibility:** Low. Documented as specialized legacy tool.

### 9. MongoAudit
- **Official URL:** https://github.com/stampery/mongoaudit
- **Repository:** https://github.com/stampery/mongoaudit
- **Primary Purpose:** Pentesting and security audit tool for MongoDB instances and clusters.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `pip install mongoaudit`.
- **Runtime Dependencies:** Python 3, `pymongo`.
- **CLI Functionality:** Yes (`mongoaudit`).
- **Structured Output:** JSON / Text reports.
- **Integration Feasibility:** High. Non-destructive MongoDB posture assessment.

### 10. SleuthQL
- **Official URL:** https://github.com/RhinoSecurityLabs/SleuthQL
- **Repository:** https://github.com/RhinoSecurityLabs/SleuthQL
- **Primary Purpose:** Python tool for discovering potential SQL injection vectors through passive web page analysis.
- **Maintenance Status:** Maintained by Rhino Security Labs.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `git clone https://github.com/RhinoSecurityLabs/SleuthQL`.
- **Runtime Dependencies:** Python 3, `bs4`, `requests`.
- **CLI Functionality:** Yes (`python3 sleuthql.py -u <target>`).
- **Structured Output:** Console text, CSV.
- **Integration Feasibility:** High. Completely passive analysis of DOM forms and parameters.

---

## Category 4: Directory and Content Discovery

### 1. Gobuster
- **Official URL:** https://github.com/OJ/gobuster
- **Repository:** https://github.com/OJ/gobuster
- **Primary Purpose:** High-speed directory/file, DNS, and vhost busting tool written in Go.
- **Maintenance Status:** Actively maintained (v3.6+).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install gobuster`, `go install github.com/OJ/gobuster/v3@latest`, `pacman -S gobuster`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`gobuster dir -u <url> -w <wordlist> -o <file>`).
- **Structured Output:** Text, JSON (`--format json` in recent versions).
- **Integration Feasibility:** Very High. Stable, battle-tested standard.

### 2. Feroxbuster
- **Official URL:** https://epi052.github.io/feroxbuster/
- **Repository:** https://github.com/epi052/feroxbuster
- **Primary Purpose:** Fast, simple, recursive content discovery tool written in Rust.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install feroxbuster`, `cargo install feroxbuster`, `brew install feroxbuster`.
- **Runtime Dependencies:** Rust binary (static).
- **CLI Functionality:** Yes (`feroxbuster -u <url> --json -o report.json`).
- **Structured Output:** Native JSON streaming (`--json`).
- **Integration Feasibility:** Exceptional. High-performance recursive discovery with structured NDJSON output.

### 3. Dirsearch
- **Official URL:** https://github.com/maurosoria/dirsearch
- **Repository:** https://github.com/maurosoria/dirsearch
- **Primary Purpose:** Advanced web path brute-forcer written in Python with multi-threading and smart extensions.
- **Maintenance Status:** Actively maintained (v0.4.3+).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `pip install dirsearch`, `apt-get install dirsearch`, `pkg install dirsearch`.
- **Runtime Dependencies:** Python 3, `requests`, `urllib3`, `colorama`.
- **CLI Functionality:** Yes (`dirsearch -u <url> --format=json -o report.json`).
- **Structured Output:** JSON (`--format=json`), CSV, XML, Plain text.
- **Integration Feasibility:** Exceptional. Native Python CLI fits directly into SUNSCAN ecosystem.

### 4. FFUF (Fuzz Faster U Fool)
- **Official URL:** https://github.com/ffuf/ffuf
- **Repository:** https://github.com/ffuf/ffuf
- **Primary Purpose:** Fast web fuzzer written in Go for discovering endpoints, vhosts, and parameters.
- **Maintenance Status:** Actively maintained (v2.1+).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install ffuf`, `go install github.com/ffuf/ffuf/v2@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`ffuf -u <url>/FUZZ -w <wordlist> -o report.json -of json`).
- **Structured Output:** Native JSON (`-of json`).
- **Integration Feasibility:** Exceptional. Gold standard for web fuzzing with rich JSON telemetry.

### 5. Dirb
- **Official URL:** http://dirb.sourceforge.net/
- **Repository:** https://gitlab.com/kalilinux/packages/dirb
- **Primary Purpose:** Web content scanner targeting existing web server paths via dictionary lookup.
- **Maintenance Status:** Stable / legacy maintenance in Debian/Kali.
- **Supported OS:** Linux, BSD.
- **Installation Methods:** `apt-get install dirb`.
- **Runtime Dependencies:** `libcurl`.
- **CLI Functionality:** Yes (`dirb <url> <wordlist> -o <file>`).
- **Structured Output:** Plain text log.
- **Integration Feasibility:** High. Ubiquitous on Kali/Debian systems.

### 6. Wfuzz
- **Official URL:** https://wfuzz.readthedocs.io/
- **Repository:** https://github.com/xmendez/wfuzz
- **Primary Purpose:** Web application fuzzer for finding non-linked resources, forms, and headers.
- **Maintenance Status:** Maintained on PyPI/GitHub.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pip install wfuzz`, `apt-get install wfuzz`.
- **Runtime Dependencies:** Python 3, `pycurl`.
- **CLI Functionality:** Yes (`wfuzz -c -z file,<wordlist> -f report.json,json <url>/FUZZ`).
- **Structured Output:** JSON (`-f report.json,json`), CSV, HTML.
- **Integration Feasibility:** High.

### 7. Katana
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/katana
- **Primary Purpose:** Next-generation crawling and spidering framework for web applications.
- **Maintenance Status:** Actively maintained by ProjectDiscovery.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install github.com/projectdiscovery/katana/cmd/katana@latest`.
- **Runtime Dependencies:** Go binary (optional headless Chrome for JS rendering).
- **CLI Functionality:** Yes (`katana -u <target> -j -o endpoints.json`).
- **Structured Output:** Native JSON Lines (`-j`).
- **Integration Feasibility:** Very High. Fast, modern, structured spider output.

### 8. Hakrawler
- **Official URL:** https://github.com/hakluke/hakrawler
- **Repository:** https://github.com/hakluke/hakrawler
- **Primary Purpose:** Fast Go web crawler for gathering endpoints, subdomains, and assets from URLs.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `go install github.com/hakluke/hakrawler@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`echo <url> | hakrawler -json`).
- **Structured Output:** JSON (`-json`), Plain text.
- **Integration Feasibility:** High. Lightweight piping utility.

### 9. DirBuster (Headless Mode)
- **Official URL:** https://owasp.org/www-project-dirbuster/
- **Repository:** https://gitlab.com/kalilinux/packages/dirbuster
- **Primary Purpose:** Multi-threaded Java application designed to brute force directories and file names.
- **Maintenance Status:** Stable / legacy in OWASP.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install dirbuster`.
- **Runtime Dependencies:** Java JRE >= 8.
- **CLI Functionality:** Yes (`java -jar DirBuster.jar -H -u <url> -l <wordlist>`).
- **Structured Output:** Text, CSV.
- **Integration Feasibility:** Medium. Java requirement makes CLI alternatives preferable.

### 10. Kiterunner
- **Official URL:** https://github.com/Assetnote/kiterunner
- **Repository:** https://github.com/Assetnote/kiterunner
- **Primary Purpose:** Context-aware API and content discovery tool built specifically for modern microservices.
- **Maintenance Status:** Actively maintained by Assetnote.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** Precompiled GitHub binaries, `make build`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`kr scan <url> -w routes.kite -o json`).
- **Structured Output:** JSON (`-o json`), Text.
- **Integration Feasibility:** High. Excellent for modern REST/GraphQL endpoint discovery.

---

## Category 5: DNS Reconnaissance & Subdomain Enumeration

### 1. DNSRecon
- **Official URL:** https://github.com/darkoperator/dnsrecon
- **Repository:** https://github.com/darkoperator/dnsrecon
- **Primary Purpose:** DNS enumeration and reconnaissance script (AXFR, SRV, SPF, brute force, cache snooping).
- **Maintenance Status:** Actively maintained by Carlos Perez.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install dnsrecon`, `pip install dnsrecon`.
- **Runtime Dependencies:** Python 3, `dnspython`, `netaddr`.
- **CLI Functionality:** Yes (`dnsrecon -d <domain> -j report.json`).
- **Structured Output:** JSON (`-j <file>`), CSV, XML, SQLite.
- **Integration Feasibility:** Exceptional. Comprehensive DNS analysis with native JSON output.

### 2. DNSenum
- **Official URL:** https://github.com/fwaeytens/dnsenum
- **Repository:** https://gitlab.com/kalilinux/packages/dnsenum
- **Primary Purpose:** Perl script to enumerate DNS information and discover non-contiguous IP blocks.
- **Maintenance Status:** Maintained in Debian/Kali.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `apt-get install dnsenum`.
- **Runtime Dependencies:** Perl, `Net::DNS`, `XML::Writer`.
- **CLI Functionality:** Yes (`dnsenum --enum <domain> -o report.xml`).
- **Structured Output:** XML (`-o <file>`), Text.
- **Integration Feasibility:** High. Standard tool on security distributions.

### 3. Fierce
- **Official URL:** https://github.com/mschwager/fierce
- **Repository:** https://github.com/mschwager/fierce
- **Primary Purpose:** DNS reconnaissance tool for locating non-contiguous IP space and hostnames across domains.
- **Maintenance Status:** Actively maintained (Python 3 port).
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `apt-get install fierce`, `pip install fierce`.
- **Runtime Dependencies:** Python 3, `dnspython`.
- **CLI Functionality:** Yes (`fierce --domain <domain>`).
- **Structured Output:** Plain text formatted output.
- **Integration Feasibility:** High. Pure Python implementation.

### 4. dnsx
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/dnsx
- **Primary Purpose:** Fast and multi-purpose DNS toolkit allow-listing multiple DNS queries with user-supplied resolvers.
- **Maintenance Status:** Actively maintained by ProjectDiscovery.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`dnsx -d <domain> -json -o output.json`).
- **Structured Output:** Native JSON Lines (`-json`).
- **Integration Feasibility:** Exceptional. Lightning-fast DNS probing with JSON streaming.

### 5. OWASP Amass
- **Official URL:** https://owasp.org/www-project-amass/
- **Repository:** https://github.com/owasp-amass/amass
- **Primary Purpose:** In-depth attack surface mapping and external asset discovery using open source intelligence and active reconnaissance.
- **Maintenance Status:** Actively maintained by OWASP.
- **Supported OS:** Linux, macOS, Windows, Docker.
- **Installation Methods:** `apt-get install amass`, `go install github.com/owasp-amass/amass/v4/...@master`, `brew install amass`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`amass enum -d <domain> -json report.json`).
- **Structured Output:** JSON (`-json <file>`), CSV, Gephi graph.
- **Integration Feasibility:** High. Comprehensive graph-based asset inventory.

### 6. Subfinder
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/subfinder
- **Primary Purpose:** Fast passive subdomain enumeration tool using passive online OSINT sources.
- **Maintenance Status:** Actively maintained by ProjectDiscovery.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`, `brew install subfinder`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`subfinder -d <domain> -oJ -o subdomains.json`).
- **Structured Output:** Native JSON (`-oJ`), Plain text.
- **Integration Feasibility:** Exceptional. Completely non-intrusive passive subdomain discovery.

### 7. Assetfinder
- **Official URL:** https://github.com/tomnomnom/assetfinder
- **Repository:** https://github.com/tomnomnom/assetfinder
- **Primary Purpose:** Lightweight utility to find domains and subdomains related to a given target.
- **Maintenance Status:** Maintained by TomNomNom.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `go install github.com/tomnomnom/assetfinder@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`assetfinder --subs-only <domain>`).
- **Structured Output:** Line-delimited text.
- **Integration Feasibility:** High. Fast, zero-overhead passive discovery.

### 8. Dig (Domain Information Groper / BIND utilities)
- **Official URL:** https://www.isc.org/bind/
- **Repository:** https://gitlab.isc.org/isc-projects/bind9
- **Primary Purpose:** Flexible CLI tool for interrogating DNS name servers and verifying record integrity.
- **Maintenance Status:** Actively maintained (core internet infrastructure).
- **Supported OS:** Linux (Debian, Ubuntu, RHEL, Termux), macOS, Windows.
- **Installation Methods:** `apt-get install dnsutils` / `bind-utils`, `pkg install dnsutils`.
- **Runtime Dependencies:** C standard library, OpenSSL.
- **CLI Functionality:** Yes (`dig ANY <domain> +noall +answer`).
- **Structured Output:** Text, YAML/JSON in modern BIND 9.18+ (`dig +yaml`).
- **Integration Feasibility:** Very High. Ubiquitous across virtually all POSIX systems.

### 9. MassDNS
- **Official URL:** https://github.com/blechschmidt/massdns
- **Repository:** https://github.com/blechschmidt/massdns
- **Primary Purpose:** High-performance DNS stub resolver capable of resolving millions of addresses per minute.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** Source build (`make`), Docker.
- **Runtime Dependencies:** C standard library.
- **CLI Functionality:** Yes (`massdns -r resolvers.txt -t A -o J domains.txt`).
- **Structured Output:** JSON (`-o J`), Text format.
- **Integration Feasibility:** High for bulk resolver verification.

### 10. Dnswalk
- **Official URL:** https://github.com/drizzt/dnswalk
- **Repository:** https://gitlab.com/kalilinux/packages/dnswalk
- **Primary Purpose:** DNS debugger that performs zone transfers and checks database for consistency and misconfigurations.
- **Maintenance Status:** Maintained in Debian/Kali.
- **Supported OS:** Linux.
- **Installation Methods:** `apt-get install dnswalk`.
- **Runtime Dependencies:** Perl, `Net::DNS`.
- **CLI Functionality:** Yes (`dnswalk <domain>.`).
- **Structured Output:** Text log.
- **Integration Feasibility:** Medium. Valuable for finding dangling CNAMEs and lame delegations.

---

## Category 6: SSL/TLS Analysis

### 1. testssl.sh
- **Official URL:** https://testssl.sh/
- **Repository:** https://github.com/drwetter/testssl.sh
- **Primary Purpose:** Free command-line tool which checks a server's service on any port for TLS/SSL ciphers, protocols, and cryptographic flaws (Heartbleed, POODLE, ROBOT, SWEET32).
- **Maintenance Status:** Actively maintained (v3.2+).
- **Supported OS:** Linux, macOS, BSD, Termux.
- **Installation Methods:** `apt-get install testssl.sh`, `git clone`, Docker.
- **Runtime Dependencies:** Bash (>= 3.2), OpenSSL binary.
- **CLI Functionality:** Yes (`testssl.sh --json-pretty <target>`).
- **Structured Output:** JSON (`--json` / `--json-pretty`), CSV, HTML.
- **Integration Feasibility:** Exceptional. Pure Bash implementation with rich JSON output.

### 2. SSLScan
- **Official URL:** https://github.com/rbsec/sslscan
- **Repository:** https://github.com/rbsec/sslscan
- **Primary Purpose:** Fast C-based tool that queries SSL/TLS services and reports supported cipher suites and server preferences.
- **Maintenance Status:** Actively maintained (v2.1+).
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install sslscan`, `pacman -S sslscan`, source build.
- **Runtime Dependencies:** `openssl`, `zlib`.
- **CLI Functionality:** Yes (`sslscan --xml=report.xml <target>`).
- **Structured Output:** XML (`--xml=<file>`), Console text with ANSI color.
- **Integration Feasibility:** High. Fast, native, lightweight scanner.

### 3. SSLyze
- **Official URL:** https://github.com/nabla-c0d3/sslyze
- **Repository:** https://github.com/nabla-c0d3/sslyze
- **Primary Purpose:** Python library and CLI tool for analyzing TLS configurations and certificates against compliance baselines (Mozilla, NIST).
- **Maintenance Status:** Actively maintained (v5.2+).
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pip install sslyze`.
- **Runtime Dependencies:** Python 3.10+, `cryptography`, `tls-parser`.
- **CLI Functionality:** Yes (`sslyze --json_out=output.json <target>`).
- **Structured Output:** Native JSON.
- **Integration Feasibility:** Exceptional.

### 4. OpenSSL s_client
- **Official URL:** https://www.openssl.org/
- **Repository:** https://github.com/openssl/openssl
- **Primary Purpose:** Standard diagnostic client for initiating SSL/TLS handshakes, viewing certificate chains, and testing specific ciphers.
- **Maintenance Status:** Actively maintained (OpenSSL 3.x).
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install openssl`, `pkg install openssl`.
- **Runtime Dependencies:** OpenSSL library.
- **CLI Functionality:** Yes (`openssl s_client -connect <host>:443 -servername <host>`).
- **Structured Output:** Standard certificate PEM and diagnostic text.
- **Integration Feasibility:** Very High. Installed by default on virtually all Linux environments.

### 5. TLS-Scanner
- **Official URL:** https://github.com/tls-attacker/TLS-Scanner
- **Repository:** https://github.com/tls-attacker/TLS-Scanner
- **Primary Purpose:** Fully-featured Java-based TLS server assessment tool based on TLS-Attacker.
- **Maintenance Status:** Actively maintained by Ruhr University Bochum.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** Precompiled `.jar` or source maven build.
- **Runtime Dependencies:** Java JRE >= 11.
- **CLI Functionality:** Yes (`java -jar TLS-Server-Scanner.jar -connect <target>`).
- **Structured Output:** JSON, Text, XML.
- **Integration Feasibility:** Medium. In-depth academic cryptographic testing.

### 6. GnuTLS Utilities (gnutls-cli / certtool)
- **Official URL:** https://www.gnutls.org/
- **Repository:** https://gitlab.com/gnutls/gnutls
- **Primary Purpose:** Secure communications library utilities for verifying X.509 certificates and TLS handshakes.
- **Maintenance Status:** Actively maintained (GNU Project).
- **Supported OS:** Linux, BSD, macOS.
- **Installation Methods:** `apt-get install gnutls-bin`.
- **Runtime Dependencies:** GnuTLS libraries.
- **CLI Functionality:** Yes (`gnutls-cli -p 443 <target>`).
- **Structured Output:** Text stream.
- **Integration Feasibility:** High. Native Linux package.

### 7. CryptCheck
- **Official URL:** https://tls.cryptcheck.fr/
- **Repository:** https://github.com/aeris/cryptcheck
- **Primary Purpose:** Tool assessing cipher suites, key exchanges, and PFS parameters against modern crypto standards.
- **Maintenance Status:** Community maintained.
- **Supported OS:** Linux.
- **Installation Methods:** Docker / Ruby gem.
- **Runtime Dependencies:** Ruby, OpenSSL.
- **CLI Functionality:** Yes.
- **Structured Output:** JSON / Text.
- **Integration Feasibility:** Medium.

### 8. O-Saft (OWASP SSL Advanced Forensic Tool)
- **Official URL:** https://owasp.org/www-project-o-saft/
- **Repository:** https://github.com/OWASP/O-Saft
- **Primary Purpose:** Multi-purpose tool to show information about SSL/TLS certificates and test remote server configurations.
- **Maintenance Status:** Actively maintained by OWASP.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `git clone https://github.com/OWASP/O-Saft`, Docker.
- **Runtime Dependencies:** Perl 5, `Net::SSLeay`.
- **CLI Functionality:** Yes (`o-saft +check <target> --format=json`).
- **Structured Output:** JSON, CSV, HTML, Text.
- **Integration Feasibility:** High. Rich check catalog.

### 9. Certipy (Certificate Inspection Component)
- **Official URL:** https://github.com/ly4k/Certipy
- **Repository:** https://github.com/ly4k/Certipy
- **Primary Purpose:** Specialized Active Directory Certificate Services (AD CS) audit and enumeration utility.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `pip install certipy-ad`.
- **Runtime Dependencies:** Python 3, `impacket`, `cryptography`.
- **CLI Functionality:** Yes (`certipy find -vulnerable`).
- **Structured Output:** JSON, BloodHound graph zip.
- **Integration Feasibility:** High for enterprise AD certificate assessments.

### 10. Cipherscan
- **Official URL:** https://github.com/mozilla/cipherscan
- **Repository:** https://github.com/mozilla/cipherscan
- **Primary Purpose:** Fast TLS cipher suite discovery script created by Mozilla's Operations Security team.
- **Maintenance Status:** Maintained on GitHub.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `git clone https://github.com/mozilla/cipherscan`.
- **Runtime Dependencies:** Bash, OpenSSL.
- **CLI Functionality:** Yes (`./cipherscan -j <target>`).
- **Structured Output:** JSON (`-j`), Text.
- **Integration Feasibility:** High. Lightweight Bash script with Mozilla security guidelines.

---

## Category 7: Packet Analysis & Network Monitoring

### 1. Wireshark (Core Analysis Engine)
- **Official URL:** https://www.wireshark.org/
- **Repository:** https://gitlab.com/wireshark/wireshark
- **Primary Purpose:** The world's foremost network protocol analyzer for deep packet inspection.
- **Maintenance Status:** Actively maintained (v4.4+).
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install wireshark`, `pacman -S wireshark-qt`.
- **Runtime Dependencies:** Qt (GUI), GLib, libpcap.
- **CLI Functionality:** CLI delivered through companion tool TShark.
- **Structured Output:** Via TShark (JSON, XML).
- **Integration Feasibility:** High (via TShark interface).

### 2. TShark
- **Official URL:** https://www.wireshark.org/docs/man-pages/tshark.html
- **Repository:** https://gitlab.com/wireshark/wireshark
- **Primary Purpose:** Terminal-oriented packet capture and protocol analysis engine of Wireshark.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux (root/proot).
- **Installation Methods:** `apt-get install tshark`, `pkg install tshark`.
- **Runtime Dependencies:** `libpcap`, `glib`.
- **CLI Functionality:** Yes (`tshark -i <iface> -T json -c 10`).
- **Structured Output:** Native JSON (`-T json` / `-T ek`), XML (`-T pdml`), CSV.
- **Integration Feasibility:** Exceptional. Industry gold standard for structured packet breakdown.

### 3. Tcpdump
- **Official URL:** https://www.tcpdump.org/
- **Repository:** https://github.com/the-tcpdump-group/tcpdump
- **Primary Purpose:** Powerful command-line packet analyzer for network troubleshooting and security monitoring.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, BSD, macOS, Termux.
- **Installation Methods:** `apt-get install tcpdump`, `pkg install tcpdump`.
- **Runtime Dependencies:** `libpcap`.
- **CLI Functionality:** Yes (`tcpdump -i <iface> -c 10 -n -q`).
- **Structured Output:** PCAP binary (`-w <file>`), formatted console text.
- **Integration Feasibility:** High. Universal packet capture standard on Unix.

### 4. Zeek (formerly Bro)
- **Official URL:** https://zeek.org/
- **Repository:** https://github.com/zeek/zeek
- **Primary Purpose:** Powerful passive network traffic analyzer and security monitoring platform producing structured connection logs.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install zeek`, source build, Docker.
- **Runtime Dependencies:** C++17 compiler, Python, `libpcap`, `zlib`, `openssl`.
- **CLI Functionality:** Yes (`zeek -r capture.pcap`).
- **Structured Output:** Tab-separated TSV / JSON logs (`conn.log`, `http.log`, `dns.log`, `ssl.log`).
- **Integration Feasibility:** Very High for offline PCAP security analysis.

### 5. Suricata
- **Official URL:** https://suricata.io/
- **Repository:** https://github.com/OISF/suricata
- **Primary Purpose:** High-performance Network IDS, IPS, and network security monitoring engine.
- **Maintenance Status:** Actively maintained by OISF.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install suricata`, PPA, source build.
- **Runtime Dependencies:** `libpcap`, `libnet`, `libyaml`, `pcre2`, `rust` (engine components).
- **CLI Functionality:** Yes (`suricata -r capture.pcap -l /tmp/suricata-logs`).
- **Structured Output:** EVE JSON (`eve.json`) containing unified alerts and protocol events.
- **Integration Feasibility:** Very High for automated rule-based PCAP analysis.

### 6. Arkime (formerly Moloch)
- **Official URL:** https://arkime.com/
- **Repository:** https://github.com/arkime/arkime
- **Primary Purpose:** Large-scale, full packet capturing, indexing, and database storage system.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux.
- **Installation Methods:** `.deb` / `.rpm` release packages.
- **Runtime Dependencies:** Elasticsearch/OpenSearch, Node.js, `libpcap`.
- **CLI Functionality:** Yes (`arkime_capture`).
- **Structured Output:** Elasticsearch JSON documents.
- **Integration Feasibility:** Medium. Enterprise-scale system; SUNSCAN integrates via PCAP parsing adapters.

### 7. ngrep (Network Grep)
- **Official URL:** https://github.com/jpr5/ngrep
- **Repository:** https://github.com/jpr5/ngrep
- **Primary Purpose:** Network packet analyzer providing GNU grep-like regular expression matching across network payloads.
- **Maintenance Status:** Actively maintained in Linux distributions.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install ngrep`.
- **Runtime Dependencies:** `libpcap`, `pcre`.
- **CLI Functionality:** Yes (`ngrep -q -W byline 'GET|POST' port 80`).
- **Structured Output:** Text stream.
- **Integration Feasibility:** High. Safe, fast pattern matching in network traffic.

### 8. Termshark
- **Official URL:** https://termshark.org/
- **Repository:** https://github.com/gcla/termshark
- **Primary Purpose:** Terminal user-interface (TUI) for TShark, inspired by Wireshark.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install github.com/gcla/termshark/v2/cmd/termshark@latest`, `brew install termshark`.
- **Runtime Dependencies:** TShark binary.
- **CLI Functionality:** Yes (`termshark -r capture.pcap`).
- **Structured Output:** Interactive terminal UI.
- **Integration Feasibility:** High. Terminal-native companion to TShark.

### 9. Netsniff-ng
- **Official URL:** http://netsniff-ng.org/
- **Repository:** https://github.com/netsniff-ng/netsniff-ng
- **Primary Purpose:** High-performance Linux network toolkit utilizing zero-copy packet sockets.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux.
- **Installation Methods:** `apt-get install netsniff-ng`.
- **Runtime Dependencies:** Linux kernel packet socket `mmap(2)`, `libnl`.
- **CLI Functionality:** Yes (`netsniff-ng --in eth0 --out dump.pcap --silent`).
- **Structured Output:** PCAP format.
- **Integration Feasibility:** Medium. Linux-specific raw packet performance engine.

### 10. Snort
- **Official URL:** https://www.snort.org/
- **Repository:** https://github.com/snort3/snort3
- **Primary Purpose:** Open source network intrusion detection and prevention system (NIDS).
- **Maintenance Status:** Actively maintained (Snort 3).
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install snort`, source build.
- **Runtime Dependencies:** `daq`, `libpcap`, `libdnet`, `luajit`.
- **CLI Functionality:** Yes (`snort -c snort.lua -r capture.pcap -A alert_json`).
- **Structured Output:** JSON alert format, unified2 binary.
- **Integration Feasibility:** High for signature-based packet assessment.

---

## Category 8: Network Enumeration & Protocol Auditing

### 1. Enum4linux-ng
- **Official URL:** https://github.com/cddmp/enum4linux-ng
- **Repository:** https://github.com/cddmp/enum4linux-ng
- **Primary Purpose:** Next-generation Windows/Samba active network enumeration tool written in Python 3.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `pip install enum4linux-ng`, `apt-get install enum4linux-ng`.
- **Runtime Dependencies:** Python 3, `impacket`, Samba client binaries (`smbclient`, `rpcclient`, `net`).
- **CLI Functionality:** Yes (`enum4linux-ng -A <target> -oJ report.json`).
- **Structured Output:** Native JSON (`-oJ` / `-oY` YAML).
- **Integration Feasibility:** Exceptional. Clean, modern replacement for legacy Perl script.

### 2. NetExec (nxc - successor to CrackMapExec)
- **Official URL:** https://www.netexec.org/
- **Repository:** https://github.com/Pennyw0rth/NetExec
- **Primary Purpose:** Automated network protocol service enumerator and posture auditor (SMB, WMI, LDAP, RDP, MSSQL, SSH).
- **Maintenance Status:** Actively maintained (the official, active community fork of CME).
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pipx install netexec`, `apt-get install netexec`.
- **Runtime Dependencies:** Python 3.10+, `impacket`, `cryptography`.
- **CLI Functionality:** Yes (`nxc smb <target>`).
- **Structured Output:** Console tabular, SQLite workspace logging.
- **Integration Feasibility:** High. Authoritative standard for protocol posture auditing.

### 3. SMBClient
- **Official URL:** https://www.samba.org/
- **Repository:** https://git.samba.org/?p=samba.git
- **Primary Purpose:** Native Samba FTP-like client to access SMB/CIFS resources on servers.
- **Maintenance Status:** Actively maintained (Samba core project).
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install smbclient`, `pacman -S smbclient`.
- **Runtime Dependencies:** Samba runtime libraries.
- **CLI Functionality:** Yes (`smbclient -L //<target> -N`).
- **Structured Output:** Delimited text.
- **Integration Feasibility:** High. Standard Linux utility for inspecting null session access.

### 4. RPCClient
- **Official URL:** https://www.samba.org/
- **Repository:** https://git.samba.org/?p=samba.git
- **Primary Purpose:** Part of Samba suite for executing MS-RPC functions on Windows NT domains.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `apt-get install smbclient`.
- **Runtime Dependencies:** Samba libraries.
- **CLI Functionality:** Yes (`rpcclient -U "" -N <target> -c "enumdomusers"`).
- **Structured Output:** Delimited text.
- **Integration Feasibility:** High for testing MSRPC permissions and anonymous binds.

### 5. SMBMap
- **Official URL:** https://github.com/ShawnDEvans/smbmap
- **Repository:** https://github.com/ShawnDEvans/smbmap
- **Primary Purpose:** Handy SMB share enumeration tool that inspects permissions across entire domains.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `apt-get install smbmap`, `pip install smbmap`.
- **Runtime Dependencies:** Python 3, `impacket`.
- **CLI Functionality:** Yes (`smbmap -H <target> -u guest`).
- **Structured Output:** Tabular console text, CSV export.
- **Integration Feasibility:** High. Excellent for verifying share read/write permissions.

### 6. Ldapsearch (OpenLDAP clients)
- **Official URL:** https://www.openldap.org/
- **Repository:** https://git.openldap.org/openldap/openldap
- **Primary Purpose:** Shell-accessible interface to the `ldap_search_ext(3)` API for directory queries.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install ldap-utils`, `pkg install openldap`.
- **Runtime Dependencies:** OpenLDAP client libraries, OpenSSL.
- **CLI Functionality:** Yes (`ldapsearch -x -H ldap://<target> -s base namingcontexts`).
- **Structured Output:** LDIF (LDAP Data Interchange Format), easily parsed into JSON.
- **Integration Feasibility:** Very High. Safe, standard directory query tool.

### 7. SNMPwalk (Net-SNMP)
- **Official URL:** http://www.net-snmp.org/
- **Repository:** https://github.com/net-snmp/net-snmp
- **Primary Purpose:** Application that uses SNMP GETNEXT requests to query a network entity for a tree of information.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install snmp`, `pkg install net-snmp`.
- **Runtime Dependencies:** Net-SNMP libraries.
- **CLI Functionality:** Yes (`snmpwalk -v 2c -c public <target> system`).
- **Structured Output:** MIB text, key-value formatted output.
- **Integration Feasibility:** High for verifying community string exposure and device telemetry.

### 8. Impacket (Examples Suite)
- **Official URL:** https://www.secureauth.com/
- **Repository:** https://github.com/fortra/impacket
- **Primary Purpose:** Collection of Python classes for working with network protocols (SMB1-3, MSRPC, Kerberos, LDAP).
- **Maintenance Status:** Actively maintained by Fortra.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `pip install impacket`, `apt-get install python3-impacket`.
- **Runtime Dependencies:** Python 3, `pycryptodomex`, `pyasn1`.
- **CLI Functionality:** Yes (suite includes `samrdump.py`, `rpcdump.py`, `lookupsid.py`).
- **Structured Output:** Console text.
- **Integration Feasibility:** High. Core underlying engine for Windows network enumeration.

### 9. Responder (Analyze Mode)
- **Official URL:** https://github.com/SpiderLabs/Responder
- **Repository:** https://github.com/SpiderLabs/Responder
- **Primary Purpose:** LLMNR, NBT-NS, and MDNS poisoner and network protocol analyzer.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux.
- **Installation Methods:** `apt-get install responder`, `git clone`.
- **Runtime Dependencies:** Python 3.
- **CLI Functionality:** Yes (`responder -I eth0 -A` in passive Analyze mode).
- **Structured Output:** Log files.
- **Integration Feasibility:** Medium. SUNSCAN permits passive analysis mode (`-A`) only to protect network safety.

### 10. NBTScan
- **Official URL:** http://unixwiz.net/tools/nbtscan.html
- **Repository:** https://github.com/resurrecting-open-source-projects/nbtscan
- **Primary Purpose:** Command-line tool that scans IP networks for NetBIOS name information.
- **Maintenance Status:** Maintained in Debian/Kali.
- **Supported OS:** Linux, macOS, BSD.
- **Installation Methods:** `apt-get install nbtscan`.
- **Runtime Dependencies:** C standard library.
- **CLI Functionality:** Yes (`nbtscan -v <cidr>`).
- **Structured Output:** Plain text, tabular NetBIOS response list.
- **Integration Feasibility:** High. Lightweight legacy network identifier.

---

## Category 9: Vulnerability Assessment

### 1. Nuclei (Vulnerability Engine)
- **Official URL:** https://projectdiscovery.io/
- **Repository:** https://github.com/projectdiscovery/nuclei
- **Primary Purpose:** Fast, community-driven vulnerability scanner with extensive coverage for CVEs, default credentials, and misconfigurations.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`nuclei -target <url> -severity low,medium,high,critical -j`).
- **Structured Output:** JSON Lines (`-j`), Markdown, SARIF.
- **Integration Feasibility:** Exceptional. Primary engine for structured vulnerability telemetry.

### 2. Trivy
- **Official URL:** https://trivy.dev/
- **Repository:** https://github.com/aquasecurity/trivy
- **Primary Purpose:** Comprehensive security scanner for container images, file systems, Git repositories, and Kubernetes configs.
- **Maintenance Status:** Actively maintained by Aqua Security.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install trivy`, `brew install trivy`, script installer.
- **Runtime Dependencies:** Go static binary.
- **CLI Functionality:** Yes (`trivy fs --format json -o report.json .`).
- **Structured Output:** Native JSON (`--format json`), SARIF, CycloneDX SBOM.
- **Integration Feasibility:** Exceptional. Essential for modern container/code posture audits.

### 3. Grype
- **Official URL:** https://github.com/anchore/grype
- **Repository:** https://github.com/anchore/grype
- **Primary Purpose:** Vulnerability scanner for container images and filesystems, paired with Syft SBOM generator.
- **Maintenance Status:** Actively maintained by Anchore.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh`, `brew install grype`.
- **Runtime Dependencies:** Go static binary.
- **CLI Functionality:** Yes (`grype dir:. -o json`).
- **Structured Output:** Native JSON (`-o json`), SARIF, CycloneDX.
- **Integration Feasibility:** Very High. Fast local software composition analysis.

### 4. OSV-Scanner
- **Official URL:** https://osv.dev/
- **Repository:** https://github.com/google/osv-scanner
- **Primary Purpose:** Official Google CLI vulnerability scanner utilizing the Open Source Vulnerabilities (OSV) database.
- **Maintenance Status:** Actively maintained by Google.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `go install github.com/google/osv-scanner/cmd/osv-scanner@latest`, GitHub releases.
- **Runtime Dependencies:** Go binary.
- **CLI Functionality:** Yes (`osv-scanner --json -r .`).
- **Structured Output:** Native JSON (`--json`), SARIF.
- **Integration Feasibility:** Exceptional. High accuracy with zero noise.

### 5. Lynis
- **Official URL:** https://cisofy.com/lynis/
- **Repository:** https://github.com/CISOfy/lynis
- **Primary Purpose:** Security auditing and hardening tool for Unix/Linux systems (compliance, CIS benchmarks).
- **Maintenance Status:** Actively maintained by CISOfy.
- **Supported OS:** Linux, macOS, BSD, Solaris.
- **Installation Methods:** `apt-get install lynis`, `pkg install lynis`, `git clone`.
- **Runtime Dependencies:** POSIX shell (sh/bash).
- **CLI Functionality:** Yes (`lynis audit system --quick --report-file report.dat`).
- **Structured Output:** Key-value report file (`/var/log/lynis-report.dat`), easily mapped to JSON.
- **Integration Feasibility:** Very High. Pure shell script host auditor.

### 6. Greenbone / OpenVAS (CLI Wrapper: gvm-cli)
- **Official URL:** https://www.greenbone.net/en/
- **Repository:** https://github.com/greenbone/gvm-tools
- **Primary Purpose:** Enterprise vulnerability management platform with 100k+ vulnerability tests.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, Docker.
- **Installation Methods:** `apt-get install gvm`, `pip install gvm-tools`.
- **Runtime Dependencies:** Python 3, PostgreSQL, Redis, GVM daemon.
- **CLI Functionality:** Yes (`gvm-cli socket --xml "<get_version/>"`).
- **Structured Output:** GMP XML.
- **Integration Feasibility:** Medium. Heavyweight service; integrated via API adapter.

### 7. Tenable Nessus (CLI / REST API)
- **Official URL:** https://www.tenable.com/products/nessus
- **Repository:** Commercial proprietary engine with public API.
- **Primary Purpose:** Commercial vulnerability assessment scanner.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, Windows, macOS.
- **Installation Methods:** `.deb` package download, Docker.
- **Runtime Dependencies:** Nessus daemon.
- **CLI Functionality:** Yes (`nessuscli`, REST API).
- **Structured Output:** `.nessus` XML, CSV, JSON (via API).
- **Integration Feasibility:** Medium. SUNSCAN supports parsing exported `.nessus` XML reports into AI summaries.

### 8. OWASP Dependency-Check
- **Official URL:** https://owasp.org/www-project-dependency-check/
- **Repository:** https://github.com/jeremylong/DependencyCheck
- **Primary Purpose:** Software Composition Analysis (SCA) tool detecting publicly disclosed vulnerabilities in application dependencies.
- **Maintenance Status:** Actively maintained by OWASP.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** Download CLI archive, `brew install dependency-check`.
- **Runtime Dependencies:** Java JRE >= 11.
- **CLI Functionality:** Yes (`dependency-check.sh --project "test" --scan . --format JSON`).
- **Structured Output:** JSON (`--format JSON`), XML, HTML, CSV.
- **Integration Feasibility:** High. Standard SCA baseline.

### 9. Clair
- **Official URL:** https://github.com/quay/clair
- **Repository:** https://github.com/quay/clair
- **Primary Purpose:** Vulnerability static analysis for container layers from Quay/Red Hat.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, Docker.
- **Installation Methods:** `go install`, Docker container.
- **Runtime Dependencies:** PostgreSQL, Go binary.
- **CLI Functionality:** Yes (`clairctl report <image>`).
- **Structured Output:** JSON.
- **Integration Feasibility:** Medium. Best suited for container pipeline integrations.

### 10. Nikto (Vulnerability Mapping)
- **Official URL:** https://cirt.net/Nikto2
- **Repository:** https://github.com/sullo/nikto
- **Primary Purpose:** Web server vulnerability assessment identifying outdated components and configuration weaknesses.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `apt-get install nikto`.
- **Runtime Dependencies:** Perl.
- **CLI Functionality:** Yes (`nikto -h <target> -Format json`).
- **Structured Output:** JSON.
- **Integration Feasibility:** High.

---

## Category 10: OSINT & Reconnaissance

### 1. theHarvester
- **Official URL:** https://github.com/laramies/theHarvester
- **Repository:** https://github.com/laramies/theHarvester
- **Primary Purpose:** OSINT tool for gathering emails, subdomains, hosts, employee names, and open ports from public sources.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `apt-get install theharvester`, `pip install theHarvester`.
- **Runtime Dependencies:** Python 3.10+, `aiodns`, `aiohttp`, `beautifulsoup4`.
- **CLI Functionality:** Yes (`theHarvester -d <domain> -b all -f report.json`).
- **Structured Output:** JSON (`-f report.json`), XML.
- **Integration Feasibility:** Exceptional. Pure Python OSINT standard.

### 2. Sherlock
- **Official URL:** https://sherlock-project.github.io/
- **Repository:** https://github.com/sherlock-project/sherlock
- **Primary Purpose:** Hunt down social media accounts by username across 400+ online platforms.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `pip install sherlock-project`, `apt-get install sherlock`.
- **Runtime Dependencies:** Python 3, `requests`, `requests-futures`.
- **CLI Functionality:** Yes (`sherlock <username> --json report.json`).
- **Structured Output:** JSON (`--json`), CSV, TXT.
- **Integration Feasibility:** Exceptional. Completely passive, safe, and structured.

### 3. Maigret
- **Official URL:** https://github.com/soxoj/maigret
- **Repository:** https://github.com/soxoj/maigret
- **Primary Purpose:** Advanced username OSINT search on steroids, generating comprehensive dossier reports from 3000+ sites.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `pip install maigret`.
- **Runtime Dependencies:** Python 3, `aiohttp`, `jinja2`.
- **CLI Functionality:** Yes (`maigret <username> --json report.json`).
- **Structured Output:** JSON (`--json`), HTML, PDF, CSV.
- **Integration Feasibility:** High. Rich structured dossiers.

### 4. Recon-ng
- **Official URL:** https://github.com/lanmaster53/recon-ng
- **Repository:** https://github.com/lanmaster53/recon-ng
- **Primary Purpose:** Full-featured Web Reconnaissance framework with independent modules, database interaction, and reporting.
- **Maintenance Status:** Actively maintained by Tim Tomes.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `apt-get install recon-ng`, `pip install recon-ng`.
- **Runtime Dependencies:** Python 3, SQLite.
- **CLI Functionality:** Yes (`recon-cli -m <module> -o <options> -x`).
- **Structured Output:** SQLite database, JSON/CSV export.
- **Integration Feasibility:** High. Modular architecture.

### 5. SpiderFoot
- **Official URL:** https://www.spiderfoot.net/
- **Repository:** https://github.com/smicallef/spiderfoot
- **Primary Purpose:** Open source OSINT automation tool integrating 200+ data sources for IP, domain, email, and phone intelligence.
- **Maintenance Status:** Maintained on GitHub.
- **Supported OS:** Linux, macOS, Windows, Docker.
- **Installation Methods:** `pip install spiderfoot`, `git clone`.
- **Runtime Dependencies:** Python 3.
- **CLI Functionality:** Yes (`sf.py -s <target> -m <modules> -o json`).
- **Structured Output:** JSON (`-o json`), CSV.
- **Integration Feasibility:** High. Massive data correlation capability.

### 6. Maltego CE (API / Data Integrator)
- **Official URL:** https://www.maltego.com/
- **Repository:** Proprietary client with public transforms.
- **Primary Purpose:** Interactive graph data mining tool for link analysis in investigative workflows.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows.
- **Installation Methods:** `.deb` download, package repos.
- **Runtime Dependencies:** Java JRE >= 11.
- **CLI Functionality:** GUI primary, CLI transform runners available.
- **Structured Output:** Graph XML (`.mtgx`), CSV.
- **Integration Feasibility:** Medium. Graph export analysis support.

### 7. Photon
- **Official URL:** https://github.com/s0md3v/Photon
- **Repository:** https://github.com/s0md3v/Photon
- **Primary Purpose:** Incredibly fast crawler designed for OSINT extracting URLs, emails, files, and social accounts.
- **Maintenance Status:** Maintained on GitHub.
- **Supported OS:** Linux, macOS, Termux.
- **Installation Methods:** `git clone https://github.com/s0md3v/Photon`, `pip install -r requirements.txt`.
- **Runtime Dependencies:** Python 3, `requests`, `urllib3`.
- **CLI Functionality:** Yes (`python3 photon.py -u <target> --export=json`).
- **Structured Output:** JSON (`--export=json`), Text files.
- **Integration Feasibility:** High. Lightweight passive OSINT.

### 8. Metagoofil
- **Official URL:** https://github.com/laramies/metagoofil
- **Repository:** https://github.com/opsdisk/metagoofil
- **Primary Purpose:** Information gathering tool designed for extracting metadata of public documents (pdf, doc, xls, ppt).
- **Maintenance Status:** Maintained by community / opsdisk fork.
- **Supported OS:** Linux, macOS.
- **Installation Methods:** `apt-get install metagoofil`, `pip install metagoofil`.
- **Runtime Dependencies:** Python 3, `pdfminer`, `openpyxl`.
- **CLI Functionality:** Yes (`metagoofil -d <domain> -t pdf,docx -l 20 -o output_dir`).
- **Structured Output:** HTML, CSV metadata reports.
- **Integration Feasibility:** High. Identifies usernames, software versions, and internal paths.

### 9. Holehe
- **Official URL:** https://github.com/megadose/holehe
- **Repository:** https://github.com/megadose/holehe
- **Primary Purpose:** Checks if an email address is registered on 120+ online services (Twitter, Instagram, GitHub, etc.) without alerting the target.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Termux.
- **Installation Methods:** `pip install holehe`.
- **Runtime Dependencies:** Python 3, `httpx`, `trio`.
- **CLI Functionality:** Yes (`holehe <email> --only-used`).
- **Structured Output:** JSON exportable, colored terminal output.
- **Integration Feasibility:** Very High. Pure Python, fast, and passive.

### 10. Social Analyzer
- **Official URL:** https://github.com/qeeqbox/social-analyzer
- **Repository:** https://github.com/qeeqbox/social-analyzer
- **Primary Purpose:** API, CLI, and Web App for analyzing and finding a person's profile across 1000+ social media websites.
- **Maintenance Status:** Actively maintained.
- **Supported OS:** Linux, macOS, Windows, Docker.
- **Installation Methods:** `pip install social-analyzer`.
- **Runtime Dependencies:** Python 3, Node.js (optional for JS rendering).
- **CLI Functionality:** Yes (`social-analyzer --username <name> --metadata`).
- **Structured Output:** JSON, CSV.
- **Integration Feasibility:** High. Multi-platform correlation.

---

## Additional Categories (11 - 20) Summary & Verified Tools

### 11. Wireless Security Analysis
1. **Aircrack-ng:** 802.11 WEP and WPA/WPA2-PSK key analysis suite (`apt-get install aircrack-ng`).
2. **Kismet:** Wireless network and device detector, sniffer, and WIDS (`apt-get install kismet`).
3. **Wifite2:** Automated wireless auditor (`apt-get install wifite`).
4. **Airgeddon:** Multi-use bash script for wireless auditing (`git clone`).
5. **Reaver:** WPS brute force auditor (`apt-get install reaver`).
6. **Bully:** C implementation of WPS brute force (`apt-get install bully`).
7. **Horst:** Lightweight IEEE802.11 wireless LAN analyzer with ncurses TUI (`apt-get install horst`).
8. **EAPHammer:** Targeted evil twin attacks and WPA-Enterprise auditing (`git clone`).
9. **Bettercap:** Swiss army knife for 802.11, BLE, and Ethernet monitoring (`apt-get install bettercap`).
10. **Pixiewps:** C tool to bruteforce WPS PINs offline (`apt-get install pixiewps`).

### 12. Password Security Auditing (Defensive Validation)
1. **John the Ripper:** Fast password security auditor and hash identifier (`apt-get install john`).
2. **Hashcat:** Advanced CPU/GPU password recovery utility (`apt-get install hashcat`).
3. **Hydra:** Fast network login security auditor (`apt-get install hydra`).
4. **Medusa:** Speedy, parallel, modular network login auditor (`apt-get install medusa`).
5. **Ncrack:** High-speed network authentication cracking tool by Nmap team (`apt-get install ncrack`).
6. **Ophcrack:** Windows password auditor using Rainbow Tables (`apt-get install ophcrack`).
7. **Cewl:** Custom wordlist generator spidering targets (`apt-get install cewl`).
8. **Crunch:** Wordlist generator (`apt-get install crunch`).
9. **HashID:** Identifies the different types of hashes (`pip install hashid`).
10. **Hash-Identifier:** Python tool to identify hash types (`apt-get install hash-identifier`).

### 13. Digital Forensics
1. **Autopsy:** Digital forensics platform (`apt-get install autopsy`).
2. **Sleuth Kit (TSK):** Library and collection of command-line tools for forensic analysis (`apt-get install sleuthkit`).
3. **Volatility 3:** Advanced memory forensics framework (`pip install volatility3`).
4. **Foremost:** Forensic program to recover lost files based on headers/footers (`apt-get install foremost`).
5. **Scalpel:** Fast file carver (`apt-get install scalpel`).
6. **Binwalk:** Firmware analysis tool (`apt-get install binwalk`).
7. **ExifTool:** Read and write meta information in files (`apt-get install libimage-exiftool-perl`).
8. **Bulk_extractor:** High speed feature extractor for forensic images (`apt-get install bulk-extractor`).
9. **Guymager:** Forensic imaging tool (`apt-get install guymager`).
10. **TestDisk & PhotoRec:** Data recovery and partition reconstruction (`apt-get install testdisk`).

### 14. Malware Analysis
1. **YARA:** The pattern matching swiss knife for malware researchers (`apt-get install yara`).
2. **Cuckoo Sandbox:** Automated malware analysis system (`pip install cuckoo`).
3. **CAPAv:** Identifies capabilities in executable files (`github.com/mandiant/capa`).
4. **FLOSS (FireEye Labs Obfuscated String Solver):** Automatically deobfuscates strings in malware (`github.com/mandiant/flare-floss`).
5. **ClamAV:** Open source antivirus engine (`apt-get install clamav`).
6. **Pefile:** Python module to parse and work with Portable Executable (PE) files (`pip install pefile`).
7. **Ghidra Headless:** Automated binary decompilation in batch mode (`apt-get install ghidra`).
8. **Radare2:** Portable reverse engineering framework (`apt-get install radare2`).
9. **Oledump:** Analyze OLE / Microsoft Office files with macros (`github.com/DidierStevens`).
10. **Viper:** Binary management and analysis framework (`pip install viper-framework`).

### 15. Reverse Engineering
1. **Ghidra:** NSA's software reverse engineering suite (`ghidra`).
2. **Radare2:** Unix-centric reverse engineering framework (`radare2`).
3. **Rizin:** Fork of radare2 focusing on usability and clean API (`rizin`).
4. **Cutter:** Free and open-source GUI for Rizin (`cutter`).
5. **GDB (GNU Debugger) with GEF/PEDA:** Enhanced debugger (`apt-get install gdb`).
6. **Objdump:** Disassembler for binary files (`binutils`).
7. **Strings:** Prints the sequences of printable characters in files (`binutils`).
8. **Strace:** System call tracer for Linux processes (`apt-get install strace`).
9. **Ltrace:** Dynamic library call tracer (`apt-get install ltrace`).
10. **Frida:** Dynamic instrumentation toolkit for developers and reverse engineers (`pip install frida-tools`).

### 16. Cloud Security
1. **Prowler:** Open-source security tool to perform AWS, Azure, and GCP security best practices audits (`pip install prowler`).
2. **ScoutSuite:** Multi-cloud security-auditing tool (`pip install scoutsuite`).
3. **Checkov:** Static analysis tool for Infrastructure as Code (Terraform, CloudFormation, K8s) (`pip install checkov`).
4. **CloudMapper:** Analyzes AWS environments for security risks (`pip install cloudmapper`).
5. **CloudFox:** Automates situational awareness in cloud environments (`github.com/BishopFox/cloudfox`).
6. **Tfsec:** Security scanner for Terraform code (`github.com/aquasecurity/tfsec`).
7. **Pacu:** AWS exploitation framework for security auditing (`pip install pacu`).
8. **Steampipe:** Query cloud infrastructure using SQL (`steampipe.io`).
9. **Cartography:** Graph-based cloud asset mapper (`pip install cartography`).
10. **IAM Vulnerability Scanner (PMapper):** Principal Mapper for AWS IAM permissions (`pip install principalmapper`).

### 17. Container & Kubernetes Security
1. **Kube-bench:** Checks whether Kubernetes is deployed securely against CIS benchmarks (`github.com/aquasecurity/kube-bench`).
2. **Kube-hunter:** Hunts for security weaknesses in Kubernetes clusters (`pip install kube-hunter`).
3. **Dockle:** Container image linter for security and best practices (`github.com/goodwithtech/dockle`).
4. **Docker Bench for Security:** Script that checks for best practices around deploying Docker (`docker-bench-security`).
5. **Trivy (Container Mode):** Container image scanner (`trivy image <tag>`).
6. **Falco:** Cloud-native runtime security tool (`falco.org`).
7. **Kubesec:** Security risk analysis for Kubernetes resources (`kubesec.io`).
8. **Popeye:** Kubernetes cluster sanitizer (`github.com/derailed/popeye`).
9. **Peirates:** Kubernetes penetration testing tool (`github.com/inguardians/peirates`).
10. **Kube-audit:** Audit Kubernetes clusters against security policies (`github.com/Shopify/kubeaudit`).

### 18. Source Code Security (SAST)
1. **Semgrep:** Fast, lightweight static analysis engine for finding bugs and enforcing code standards (`pip install semgrep`).
2. **Bandit:** Security linter for Python code (`pip install bandit`).
3. **Gitleaks:** Scan git repositories for secrets and passwords (`github.com/gitleaks/gitleaks`).
4. **TruffleHog:** Find leaked credentials in code and git history (`github.com/trufflesecurity/trufflehog`).
5. **Brakeman:** Static analysis security vulnerability scanner for Ruby on Rails (`gem install brakeman`).
6. **GoSec:** Security checker for Go source code (`github.com/securego/gosec`).
7. **Flawfinder:** C/C++ source code security auditing tool (`apt-get install flawfinder`).
8. **SonarScanner CLI:** Code quality and security scanner (`sonarsource.com`).
9. **Horusec:** Open-source tool that performs SAST across multiple languages (`github.com/ZupIT/horusec`).
10. **NodeJsScan:** Static security code scanner for Node.js applications (`pip install nodejsscan`).

### 19. API Security Testing
1. **Postman / Newman CLI:** Automated collection testing for REST APIs (`npm install -g newman`).
2. **Akto:** Open-source API security platform (`github.com/akto-api-security/akto`).
3. **CherryBomb:** API security validator against OpenAPI specs (`github.com/blst-security/cherrybomb`).
4. **Astra:** Automated security testing framework for REST APIs (`pip install astra`).
5. **RESTler:** First stateful REST API fuzzing tool from Microsoft (`github.com/microsoft/restler-fuzzer`).
6. **Kiterunner:** API endpoint route bruter (`github.com/Assetnote/kiterunner`).
7. **GraphQLmap:** GraphQL endpoint security auditing tool (`github.com/swisskyrepo/GraphQLmap`).
8. **Inql:** GraphQL security scanner (`pip install inql`).
9. **Clairvoyance:** Discovers GraphQL schemas even when introspection is disabled (`pip install clairvoyance`).
10. **Fuzzapi:** API fuzzer using Wfuzz and OpenAPI (`github.com/Fuzzapi/fuzzapi`).

### 20. Active Directory Security Assessment
1. **BloodHound / BloodHound.py:** Active Directory relationship graph visualization (`pip install bloodhound`).
2. **NetExec:** Protocol posture auditor (`pipx install netexec`).
3. **Certipy:** Active Directory Certificate Services auditor (`pip install certipy-ad`).
4. **Impacket:** Network protocol suite (`pip install impacket`).
5. **Responder (Passive):** LLMNR/NBT-NS monitoring (`responder`).
6. **ADExplorer:** Sysinternals viewer for Active Directory (`Microsoft Sysinternals`).
7. **PingCastle:** Active Directory security assessment tool against health and security scorecards.
8. **ADIDNSDump:** Active Directory-integrated DNS dumping utility (`pip install adidnsdump`).
9. **PyGPOAbuse:** Active Directory GPO abuse tool (`github.com/Hackndo/pygpoabuse`).
10. **Ldapdomaindump:** Active Directory information dumper via LDAP (`pip install ldapdomaindump`).

---

## Conclusion of Phase 1
Over 200 security utilities across 20 categories have been identified, audited, and cataloged. In Phase 2 through Phase 4, SUNSCAN utilizes this empirical baseline to generate `docs/TOOL_COMPATIBILITY.md`, `docs/TOOL_INSTALLATION_MATRIX.md`, and the authoritative `docs/TOOL_CATALOG.json`.
