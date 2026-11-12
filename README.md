# SUNSCAN

> **Modular Cybersecurity Toolkit & AI-Powered Output Analyzer**  
> *"Understand Every Scan. Discover Every Risk."*  
> Developed by **CodeSun** · Licensed under **MIT**

---

## Overview

SUNSCAN is an open-source cybersecurity auditing framework and diagnostic toolkit. It brings together verified security utilities into a modular catalog, enforces unprivileged execution and target authorization validation, and provides structured AI analysis (via OpenRouter or Google Gemini) to turn raw terminal outputs into clear, evidence-based security findings in both English and Bengali.

### Core Architecture

- **CLI Distribution (`bin/sunscan.js`, `src/launcher.js`)**: Lightweight Node.js wrapper for `npm install -g sunscan-cli`.
- **Core Engine (`engine/`)**: Python architecture for target validation, process orchestration, and scan history.
- **Data Catalog (`docs/TOOL_CATALOG.json`)**: Empirical database of verified security tools, categorized by purpose and risk rating.
- **AI Analysis Engine (`ai/`)**: Structured security interpreter providing non-alarmist severity ratings, evidence quotes, and hardening recommendations.
- **Interactive Web Workbench (`src/App.tsx`, `server.ts`)**: Full-stack web dashboard with terminal simulator, tool catalog explorer, and printable report generator.

---

## Installation

### Via NPM
```bash
npm install -g sunscan-cli
```
*Note: Installing SUNSCAN never automatically downloads external cybersecurity tools. External scanners are installed individually only upon explicit user confirmation.*

### From Source
```bash
git clone https://github.com/codesun/sunscan.git
cd sunscan
npm install
npm run build
```

---

## Usage

### Interactive Terminal Interface
```bash
sunscan
```

### CLI Options
```bash
# Display system environment diagnostics
sunscan --diag

# List catalog tools and installation status
sunscan --list-tools

# Run a quick scan preset with AI output analysis
sunscan --scan nmap scanme.nmap.org --ai --lang en
```

---

## Authorization & Responsible Testing

SUNSCAN is strictly designed for authorized security posture assessments, defensive auditing, and educational verification on systems you own or are explicitly authorized to test. Destructive payloads and unverified exploit automation are strictly prohibited.
