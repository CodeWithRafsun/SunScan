# SUNSCAN Tool Installation Matrix
**Project:** SUNSCAN (Modular Cybersecurity Toolkit & AI-Powered Output Analyzer)  
**Organization:** CodeSun  
**Document:** `docs/TOOL_INSTALLATION_MATRIX.md`

---

## 1. Package Manager Detection Hierarchy

SUNSCAN executes non-intrusive environment detection in the following priority order:
1. **Termux (`pkg` / `apt`)**: Checks if `$PREFIX/bin/pkg` exists. Uses `pkg install -y <tool>`.
2. **Debian / Ubuntu / Kali (`apt`)**: Checks if `command -v apt-get` exists. Uses `sudo apt-get install -y <tool>`.
3. **Arch / BlackArch / Manjaro (`pacman`)**: Checks if `command -v pacman` exists. Uses `sudo pacman -S --noconfirm <tool>`.
4. **Fedora / RHEL / CentOS (`dnf` / `yum`)**: Checks if `command -v dnf` or `command -v yum` exists. Uses `sudo dnf install -y <tool>`.
5. **macOS (`brew`)**: Checks if `command -v brew` exists. Uses `brew install <tool>`.
6. **Python (`pip` / `pipx`)**: Used for standalone Python security utilities (`sqlmap`, `theharvester`, `dirsearch`, `sslyze`, `sherlock`, `semgrep`).
7. **Go (`go install`)**: Used for ProjectDiscovery utilities (`nuclei`, `naabu`, `subfinder`, `katana`, `dnsx`) and modern Go tools (`ffuf`, `gobuster`).
8. **Rust (`cargo install`)**: Used for Rust-based tools (`feroxbuster`, `rustscan`).

---

## 2. Verified Tool Installation Commands

| Tool ID | Tool Name | Debian/Kali (`apt`) | Termux (`pkg`) | Arch (`pacman`) | Language/Universal | Verification Command |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `nmap` | Nmap | `apt-get install -y nmap` | `pkg install -y nmap` | `pacman -S nmap` | Source / static binary | `nmap --version` |
| `masscan` | Masscan | `apt-get install -y masscan` | Root/chroot | `pacman -S masscan` | `make -j` | `masscan --version` |
| `rustscan` | RustScan | `.deb` release | Precompiled musl | `pacman -S rustscan` | `cargo install rustscan` | `rustscan --version` |
| `arp-scan` | ARP-scan | `apt-get install -y arp-scan` | Root required | `pacman -S arp-scan` | Source build | `arp-scan --version` |
| `nikto` | Nikto | `apt-get install -y nikto` | `pkg install -y nikto` | `pacman -S nikto` | Perl / git clone | `nikto -Version` |
| `whatweb` | WhatWeb | `apt-get install -y whatweb` | `pkg install -y whatweb`| `pacman -S whatweb` | `gem install whatweb` | `whatweb --version` |
| `sqlmap` | SQLMap | `apt-get install -y sqlmap` | `pkg install -y sqlmap`| `pacman -S sqlmap` | `pip install sqlmap` | `sqlmap --version` |
| `gobuster` | Gobuster | `apt-get install -y gobuster`| `go install` | `pacman -S gobuster`| `go install github.com/OJ/gobuster/v3@latest` | `gobuster version` |
| `feroxbuster`| Feroxbuster | `apt-get install -y feroxbuster`| musl binary | `pacman -S feroxbuster`| `cargo install feroxbuster` | `feroxbuster --version` |
| `dirsearch` | Dirsearch | `apt-get install -y dirsearch`| `pkg install -y dirsearch`| `pacman -S dirsearch`| `pip install dirsearch` | `dirsearch --version` |
| `ffuf` | FFUF | `apt-get install -y ffuf` | `go install` | `pacman -S ffuf` | `go install github.com/ffuf/ffuf/v2@latest` | `ffuf -V` |
| `dnsrecon` | DNSRecon | `apt-get install -y dnsrecon`| `pip install` | `pacman -S dnsrecon`| `pip install dnsrecon` | `dnsrecon -v` |
| `subfinder` | Subfinder | `.deb` release | `go install` | `pacman -S subfinder`| `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` | `subfinder -version` |
| `dnsx` | dnsx | `.deb` release | `go install` | `pacman -S dnsx` | `go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest` | `dnsx -version` |
| `testssl` | testssl.sh | `apt-get install -y testssl.sh`| `pkg install -y testssl.sh`| `pacman -S testssl.sh`| Git clone / bash | `testssl.sh -v` |
| `sslscan` | SSLScan | `apt-get install -y sslscan` | Build | `pacman -S sslscan` | Source build | `sslscan --version` |
| `sslyze` | SSLyze | `apt-get install -y sslyze` | `pip install` | `pacman -S sslyze` | `pip install sslyze` | `sslyze --version` |
| `tshark` | TShark | `apt-get install -y tshark` | `pkg install -y tshark`| `pacman -S wireshark-cli` | Distribution package | `tshark -v` |
| `tcpdump` | Tcpdump | `apt-get install -y tcpdump` | `pkg install -y tcpdump`| `pacman -S tcpdump` | Distribution package | `tcpdump --version` |
| `enum4linux-ng` | Enum4linux-ng | `apt-get install -y enum4linux-ng`| `pip install` | AUR | `pip install enum4linux-ng` | `enum4linux-ng --version` |
| `smbclient` | SMBClient | `apt-get install -y smbclient`| `pkg install -y samba`| `pacman -S smbclient` | Distribution package | `smbclient --version` |
| `nuclei` | Nuclei | `.deb` release | `go install` | `pacman -S nuclei` | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` | `nuclei -version` |
| `trivy` | Trivy | `apt-get install -y trivy` | Precompiled | `pacman -S trivy` | Standalone binary | `trivy --version` |
| `grype` | Grype | Shell script | Precompiled | `pacman -S grype` | Standalone binary | `grype version` |
| `osv-scanner`| OSV-Scanner | `.deb` release | `go install` | AUR | `go install github.com/google/osv-scanner/cmd/osv-scanner@latest` | `osv-scanner --version` |
| `lynis` | Lynis | `apt-get install -y lynis` | `pkg install -y lynis` | `pacman -S lynis` | Git clone / bash | `lynis --version` |
| `theharvester`| theHarvester | `apt-get install -y theharvester`| `pip install` | `pacman -S theharvester`| `pip install theHarvester` | `theHarvester -h` |
| `sherlock` | Sherlock | `apt-get install -y sherlock`| `pkg install -y sherlock`| `pacman -S sherlock`| `pip install sherlock-project` | `sherlock --version` |
| `holehe` | Holehe | `pip install holehe` | `pip install holehe` | AUR | `pip install holehe` | `holehe -h` |
| `semgrep` | Semgrep | `pip install semgrep` | Not recommended | `pacman -S semgrep` | `pip install semgrep` | `semgrep --version` |

---

## 3. Installation Flow & Safety Rules

1. **Zero Silent Installs**: SUNSCAN queries the local system for executable presence using `shutil.which(tool_executable)` in Python or `command -v <tool>` in Bash.
2. **Explicit Confirmation**: If an uninstalled tool is requested, SUNSCAN displays:
   - Tool description and official repository.
   - Exact command that would be executed.
   - Prompt: `Do you want to install [tool] via [detected package manager]? [y/N]`
3. **Graceful Fallback**: If installation fails or package manager is not available, SUNSCAN presents comprehensive manual installation copy-paste commands without crashing.
