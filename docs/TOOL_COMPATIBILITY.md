# SUNSCAN Platform Compatibility Guide
**Project:** SUNSCAN (Modular Cybersecurity Toolkit & AI-Powered Output Analyzer)  
**Organization:** CodeSun  
**Document:** `docs/TOOL_COMPATIBILITY.md`

---

## 1. Operating System & Platform Matrix

| Platform | Primary Kernel | Package Manager | Shell Environment | Privilege Escalation | Compatibility Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kali Linux** | Linux 6.x+ | `apt` / `dpkg` | bash / zsh | `sudo` | Tier 1 (Native Full Support) |
| **Debian 11/12** | Linux 5.x / 6.x | `apt` | bash / sh | `sudo` / `su` | Tier 1 (Native Full Support) |
| **Ubuntu 22.04 / 24.04** | Linux 5.x / 6.x | `apt` / `snap` | bash / dash | `sudo` | Tier 1 (Native Full Support) |
| **Arch / BlackArch** | Linux 6.x+ rolling | `pacman` | bash / zsh | `sudo` | Tier 1 (Native Full Support) |
| **Fedora / RHEL** | Linux 5.x / 6.x | `dnf` / `rpm` | bash | `sudo` | Tier 1 (Native Full Support) |
| **Termux (Android)** | Linux (Android userland) | `pkg` / `apt` | bash | Rootless / proot / tsu | Tier 2 (Supported with constraints) |
| **macOS (Homebrew)** | Darwin (XNU) | `brew` | zsh / bash | `sudo` | Tier 2 (Supported with constraints) |
| **Windows (WSL2)** | Linux 5.x/6.x in VM | `apt` / `dnf` | bash | `sudo` | Tier 1 (Full in WSL2) |

---

## 2. Termux Platform Constraints & Truthful Compatibility

SUNSCAN maintains strict fidelity regarding Android / Termux capabilities:
1. **Raw Sockets (`AF_INET` `SOCK_RAW`)**: Android kernels restrict raw sockets to UID 0 (root). Tools that rely on SYN stealth scanning (`nmap -sS`, `masscan`, `hping3`, `arp-scan`) will fail unless executed under `tsu` or a rooted environment.
2. **Unprivileged TCP / UDP (Connect Mode)**: Tools utilizing standard POSIX connect sockets run flawlessly rootless in Termux:
   - `nmap -sT -Pn` (TCP connect scan)
   - `whatweb`, `nikto`, `feroxbuster`, `gobuster`, `ffuf`, `dirsearch`
   - `subfinder`, `dnsx`, `dnsrecon`, `dig`
   - `theHarvester`, `sherlock`, `holehe`, `maigret`
   - `semgrep`, `bandit`, `trufflehog`
3. **Environment Flags**: SUNSCAN detects Termux via `$PREFIX` (`/data/data/com.termux/files/usr`) and automatically selects `pkg` as the primary installer and sets non-privileged defaults (`-sT` instead of `-sS`).

---

## 3. Architecture Compatibility

- **x86_64 (amd64)**: 100% of integrated tools provide precompiled binaries, packages, or straightforward source builds.
- **aarch64 / arm64** (Apple Silicon, Raspberry Pi 4/5, Modern Android Termux, ARM VPS):
  - Python tools (`sqlmap`, `theharvester`, `dirsearch`, `sslyze`, `sherlock`): 100% compatible.
  - Go tools (`nuclei`, `naabu`, `subfinder`, `katana`, `ffuf`, `gobuster`): 100% compatible via `go install` or official arm64 releases.
  - Rust tools (`feroxbuster`, `rustscan`): 100% compatible via `cargo install` or musl releases.
  - C/C++ tools (`nmap`, `tcpdump`, `tshark`, `zmap`): 100% available via distribution `apt`/`pkg` repositories.
- **armv7l (32-bit ARM)**:
  - Supported for Python, C (`nmap`, `tcpdump`), and Go tools with 32-bit ARM targets.

---

## 4. Privilege Isolation (Root vs. Rootless)

SUNSCAN enforces the principle of least privilege:
- **Never auto-elevate**: SUNSCAN will never invoke `sudo` without explicit user prompt and confirmation.
- **Rootless by Default**: All default presets (e.g. `nmap -sT`, `testssl.sh`, `subfinder`, `nikto`, `whatweb`, `feroxbuster`) are designed to run safely as an unprivileged user.
- **Privileged Presets Marked**: Advanced presets requiring raw sockets (e.g., OS fingerprinting `nmap -O`, SYN scan `nmap -sS`, ARP discovery `arp-scan`) are explicitly marked with `[REQUIRES ROOT]` badges and display authorization confirmations before execution.
