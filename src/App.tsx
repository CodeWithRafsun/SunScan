/**
 * SUNSCAN - Modular Cybersecurity Toolkit & AI-Powered Output Analyzer
 * Organization: CodeSun
 * License: MIT
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  Terminal,
  Shield,
  Layers,
  Cpu,
  FileText,
  Settings,
  Play,
  Square,
  Sparkles,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  AlertCircle,
  Info,
  Download,
  Copy,
  Check,
  RefreshCw,
  Search,
  Globe,
  Sliders,
  ChevronRight,
  Database,
  Lock,
  Radio,
  FileCode,
} from 'lucide-react';

interface ToolCommand {
  id: string;
  name: string;
  level: 'basic' | 'intermediate' | 'advanced';
  purpose: string;
  bangla_purpose?: string;
  command_template: string;
  args: string[];
  risk: 'low' | 'medium' | 'high';
  time_estimate: string;
  requires_root: boolean;
  authorization_notice: string;
}

interface ToolItem {
  id: string;
  name: string;
  category: string;
  description: string;
  bangla_description?: string;
  official_url: string;
  repository: string;
  platforms: string[];
  installers: string[];
  executable: string;
  requires_root: boolean;
  supports_json: boolean;
  supports_xml: boolean;
  commands: ToolCommand[];
  installed?: boolean;
}

interface CategoryItem {
  id: string;
  name: string;
  bangla_name?: string;
  description: string;
}

interface Finding {
  title: string;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  confidence: 'low' | 'medium' | 'high';
  evidence: string;
  explanation: string;
  impact?: string;
  recommendation: string;
}

interface AIAnalysisReport {
  summary: string;
  risk_score: 'low' | 'medium' | 'high' | 'critical';
  findings: Finding[];
  limitations?: string[];
  next_steps?: string[];
}

interface ScanRecord {
  scan_id: string;
  tool_id: string;
  tool_name: string;
  command_id: string;
  command_name: string;
  target: string;
  command_str: string;
  start_time: string;
  end_time: string;
  status: 'completed' | 'failed' | 'running';
  exit_code: number;
  raw_output: string;
  output_lines: string[];
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'workbench' | 'catalog' | 'analyzer' | 'reports' | 'diagnostics'>('workbench');
  const [language, setLanguage] = useState<'en' | 'bn'>('en');
  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [tools, setTools] = useState<ToolItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('network-scanning');
  const [selectedToolId, setSelectedToolId] = useState<string>('nmap');
  const [selectedCommandId, setSelectedCommandId] = useState<string>('');
  const [targetInput, setTargetInput] = useState<string>('scanme.nmap.org');
  const [authConfirmed, setAuthConfirmed] = useState<boolean>(false);
  const [showAuthModal, setShowAuthModal] = useState<boolean>(false);

  // Scan execution state
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [scanOutput, setScanOutput] = useState<string[]>([]);
  const [currentScanId, setCurrentScanId] = useState<string>('');
  const [scanElapsedTime, setScanElapsedTime] = useState<number>(0);
  const [lastScanRecord, setLastScanRecord] = useState<ScanRecord | null>(null);

  // AI analysis state
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [analysisReport, setAnalysisReport] = useState<AIAnalysisReport | null>(null);
  const [manualOutputInput, setManualOutputInput] = useState<string>('');

  // Diagnostics and reports
  const [diagnosticsData, setDiagnosticsData] = useState<any>(null);
  const [reportsList, setReportsList] = useState<ScanRecord[]>([]);

  // Settings
  const [openRouterKey, setOpenRouterKey] = useState<string>('');
  const [openRouterModel, setOpenRouterModel] = useState<string>('google/gemini-2.0-flash-001');
  const [showSettingsModal, setShowSettingsModal] = useState<boolean>(false);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const terminalEndRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<any>(null);

  // Load catalog on mount
  useEffect(() => {
    fetchCatalog();
    fetchDiagnostics();
    fetchReports();
  }, []);

  // Autoscroll terminal
  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [scanOutput]);

  const fetchCatalog = async () => {
    try {
      const res = await fetch('/api/catalog');
      if (res.ok) {
        const data = await res.json();
        setCategories(data.categories || []);
        setTools(data.tools || []);
        if (data.tools && data.tools.length > 0) {
          const first = data.tools[0];
          setSelectedToolId(first.id);
          if (first.commands && first.commands.length > 0) {
            setSelectedCommandId(first.commands[0].id);
          }
        }
      }
    } catch {
      // Catalog fallback
    }
  };

  const fetchDiagnostics = async () => {
    try {
      const res = await fetch('/api/diagnostics');
      if (res.ok) {
        const data = await res.json();
        setDiagnosticsData(data);
      }
    } catch {
      // Diagnostics fallback
    }
  };

  const fetchReports = async () => {
    try {
      const res = await fetch('/api/reports');
      if (res.ok) {
        const data = await res.json();
        setReportsList(data);
      }
    } catch {
      // Reports fallback
    }
  };

  const selectedTool = tools.find((t) => t.id === selectedToolId) || tools[0];
  const selectedCommand = selectedTool?.commands?.find((c) => c.id === selectedCommandId) || selectedTool?.commands?.[0];

  // Constructed command string preview
  const constructedCommand = selectedTool && selectedCommand
    ? `${selectedTool.executable} ${(selectedCommand.args || []).join(' ').replace('{target}', targetInput.trim() || '<target>')}`
    : '';

  const handleStartScan = async () => {
    if (!authConfirmed) {
      setShowAuthModal(true);
      return;
    }
    if (!targetInput.trim()) {
      return;
    }

    setIsScanning(true);
    setScanOutput([
      `[SUNSCAN] Initializing process engine for ${selectedTool?.name}...`,
      `[SUNSCAN] Validating target '${targetInput}' (RFC-1123 / IPv4 / URL conformant)`,
      `[SUNSCAN] Command: ${constructedCommand}`,
      `[SUNSCAN] Authorization confirmed. Launching scan job...`,
      ``,
    ]);
    setAnalysisReport(null);
    setScanElapsedTime(0);

    const startTs = Date.now();
    timerRef.current = setInterval(() => {
      setScanElapsedTime(Math.floor((Date.now() - startTs) / 1000));
    }, 500);

    try {
      const res = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          toolId: selectedTool?.id,
          commandId: selectedCommand?.id,
          target: targetInput.trim(),
          simulated: false,
        }),
      });

      clearInterval(timerRef.current);
      setIsScanning(false);

      if (res.ok) {
        const data: ScanRecord = await res.json();
        setLastScanRecord(data);
        setCurrentScanId(data.scan_id);
        setScanOutput(data.output_lines || [data.raw_output]);
        fetchReports();
      } else {
        const err = await res.json();
        setScanOutput((prev) => [...prev, `[ERROR] Scan failed: ${err.error}`]);
      }
    } catch (e: any) {
      clearInterval(timerRef.current);
      setIsScanning(false);
      setScanOutput((prev) => [...prev, `[ERROR] Request failure: ${e.message}`]);
    }
  };

  const handleStopScan = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    setIsScanning(false);
    setScanOutput((prev) => [...prev, `\n[SUNSCAN] Scan cancellation requested by user.`]);
  };

  const handleAnalyzeWithAI = async (customText?: string) => {
    const rawToAnalyze = customText || (lastScanRecord ? lastScanRecord.raw_output : scanOutput.join('\n'));
    if (!rawToAnalyze || rawToAnalyze.trim().length === 0) return;

    setIsAnalyzing(true);
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          toolName: selectedTool?.name || 'Security Scanner',
          target: targetInput,
          rawOutput: rawToAnalyze,
          language,
          openRouterKey,
          openRouterModel,
        }),
      });

      if (res.ok) {
        const report = await res.json();
        setAnalysisReport(report);
      } else {
        const err = await res.json();
        setAnalysisReport({
          summary: `Analysis could not be completed: ${err.error}`,
          risk_score: 'low',
          findings: [],
        });
      }
    } catch (e: any) {
      setAnalysisReport({
        summary: `Analysis request failed: ${e.message}`,
        risk_score: 'low',
        findings: [],
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const downloadJSONReport = (record: ScanRecord) => {
    const blob = new Blob([JSON.stringify(record, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sunscan-${record.scan_id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* 1. TOP BAR CONTRACT (§2 Top Bar Contract: Brand zone - 4-5 links - 1 action) */}
      <header className="flex items-center justify-between gap-8 px-6 py-3.5 border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
        {/* Zone 1: Brand wordmark (single element, no subtitle) */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="w-8 h-8 rounded bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
            <Shield className="w-4 h-4" />
          </div>
          <span className="text-lg font-bold tracking-tight text-white whitespace-nowrap">
            SUNSCAN
          </span>
        </div>

        {/* Zone 2: Navigation Links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium text-slate-400">
          <button
            onClick={() => setActiveTab('workbench')}
            className={`transition-colors whitespace-nowrap shrink-0 hover:text-white ${
              activeTab === 'workbench' ? 'text-amber-400 font-semibold' : ''
            }`}
          >
            {language === 'en' ? 'Workbench' : 'ওয়ার্কবেঞ্চ'}
          </button>
          <button
            onClick={() => setActiveTab('catalog')}
            className={`transition-colors whitespace-nowrap shrink-0 hover:text-white ${
              activeTab === 'catalog' ? 'text-amber-400 font-semibold' : ''
            }`}
          >
            {language === 'en' ? 'Tool Catalog' : 'টুল ক্যাটালগ'}
          </button>
          <button
            onClick={() => setActiveTab('analyzer')}
            className={`transition-colors whitespace-nowrap shrink-0 hover:text-white ${
              activeTab === 'analyzer' ? 'text-amber-400 font-semibold' : ''
            }`}
          >
            {language === 'en' ? 'AI Analyzer' : 'এআই অ্যানালাইজার'}
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            className={`transition-colors whitespace-nowrap shrink-0 hover:text-white ${
              activeTab === 'reports' ? 'text-amber-400 font-semibold' : ''
            }`}
          >
            {language === 'en' ? 'Reports' : 'রিপোর্টস'}
          </button>
          <button
            onClick={() => setActiveTab('diagnostics')}
            className={`transition-colors whitespace-nowrap shrink-0 hover:text-white ${
              activeTab === 'diagnostics' ? 'text-amber-400 font-semibold' : ''
            }`}
          >
            {language === 'en' ? 'Diagnostics' : 'ডায়াগনস্টিকস'}
          </button>
        </nav>

        {/* Zone 3: Single Primary Action & Settings */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={() => setLanguage(language === 'en' ? 'bn' : 'en')}
            className="text-xs px-2.5 py-1.5 rounded border border-slate-700 bg-slate-800 text-slate-300 hover:text-white hover:border-slate-600 transition-colors whitespace-nowrap shrink-0"
            title="Switch Language"
          >
            {language === 'en' ? 'বাংলা' : 'English'}
          </button>
          <button
            onClick={() => setShowSettingsModal(true)}
            className="p-1.5 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition-colors shrink-0"
            title="Settings & OpenRouter"
          >
            <Settings className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setActiveTab('workbench');
              if (authConfirmed) handleStartScan();
              else setShowAuthModal(true);
            }}
            disabled={isScanning}
            className="px-4 py-2 text-xs font-semibold text-slate-950 bg-amber-400 rounded hover:bg-amber-300 transition-colors whitespace-nowrap shrink-0 disabled:opacity-50"
          >
            {isScanning ? (language === 'en' ? 'Running Scan...' : 'স্ক্যান চলছে...') : (language === 'en' ? 'Start Scan' : 'নতুন স্ক্যান')}
          </button>
        </div>
      </header>

      {/* SUB-HEADER / BANNER */}
      <div className="border-b border-slate-800 bg-slate-900/40 px-6 py-2.5 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-3">
          <span className="font-mono text-amber-400/90 font-medium">CODESUN CYBERSECURITY</span>
          <span aria-hidden="true" className="text-slate-600">·</span>
          <span>Open-Source CLI & Defensive Auditing Engine</span>
          <span aria-hidden="true" className="text-slate-600">·</span>
          <span>MIT License</span>
        </div>
        <div className="flex items-center gap-3 font-mono text-slate-400">
          <span>Target Auth:</span>
          {authConfirmed ? (
            <span className="text-emerald-400 font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 inline" /> Verified
            </span>
          ) : (
            <button
              onClick={() => setShowAuthModal(true)}
              className="text-amber-400 underline hover:text-amber-300 transition-colors"
            >
              Verify Authorization
            </button>
          )}
        </div>
      </div>

      {/* MAIN VIEW CONTENT CONTAINER */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 flex flex-col gap-6">

        {/* TAB 1: WORKBENCH */}
        {activeTab === 'workbench' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            {/* Left Control Column (4 cols) */}
            <div className="lg:col-span-4 flex flex-col gap-5">
              {/* Target & Preset Configuration Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4">
                <h2 className="text-sm font-semibold text-white uppercase tracking-wider text-slate-300 flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-amber-400" />
                  {language === 'en' ? 'Scan Target & Profile' : 'টার্গেট ও স্ক্যান প্রোফাইল'}
                </h2>

                {/* Target Input */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-slate-400 font-medium">
                    {language === 'en' ? 'Target Host / IP / URL / CIDR' : 'টার্গেট হোস্ট / আইপি / ইউআরএল'}
                  </label>
                  <input
                    type="text"
                    value={targetInput}
                    onChange={(e) => setTargetInput(e.target.value)}
                    placeholder="e.g. scanme.nmap.org or 192.168.1.1"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400 font-mono"
                  />
                  <span className="text-[11px] text-slate-500">
                    {language === 'en' ? 'RFC-1123 Hostname, IPv4, or HTTP URL' : 'বৈধ ডোমেন বা আইপি অ্যাড্রেস'}
                  </span>
                </div>

                {/* Tool Selector */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-slate-400 font-medium">
                    {language === 'en' ? 'Diagnostic Tool' : 'ডায়াগনস্টিক টুল'}
                  </label>
                  <select
                    value={selectedToolId}
                    onChange={(e) => {
                      const newId = e.target.value;
                      setSelectedToolId(newId);
                      const t = tools.find((x) => x.id === newId);
                      if (t && t.commands?.length > 0) {
                        setSelectedCommandId(t.commands[0].id);
                      }
                    }}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400"
                  >
                    {tools.map((t) => (
                      <option key={t.id} value={t.id}>
                        {t.name} ({t.category})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Command Preset Selector */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-slate-400 font-medium">
                    {language === 'en' ? 'Command Preset' : 'কমান্ড প্রিসেট'}
                  </label>
                  <select
                    value={selectedCommandId}
                    onChange={(e) => setSelectedCommandId(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400"
                  >
                    {selectedTool?.commands?.map((c) => (
                      <option key={c.id} value={c.id}>
                        [{c.level.toUpperCase()}] {c.name} ({c.risk.toUpperCase()} Risk)
                      </option>
                    ))}
                  </select>
                </div>

                {/* Command details */}
                {selectedCommand && (
                  <div className="border border-slate-800/80 rounded bg-slate-950/60 p-3 flex flex-col gap-2 text-xs">
                    <div className="text-slate-300 font-medium">
                      {language === 'en' ? selectedCommand.purpose : (selectedCommand.bangla_purpose || selectedCommand.purpose)}
                    </div>
                    <div className="flex items-center gap-3 text-slate-400">
                      <span>Est. Duration: <strong className="text-white tabular-nums">{selectedCommand.time_estimate}</strong></span>
                      <span aria-hidden="true">·</span>
                      <span>Root required: <strong className="text-white">{selectedCommand.requires_root ? 'Yes' : 'No'}</strong></span>
                    </div>
                    <div className="text-amber-400/90 text-[11px] leading-relaxed">
                      <strong>Notice:</strong> {selectedCommand.authorization_notice}
                    </div>
                  </div>
                )}

                {/* Command Syntax Box */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-slate-400 font-medium">
                    {language === 'en' ? 'Command Syntax Preview' : 'কমান্ড সিনট্যাক্স প্রিভিউ'}
                  </label>
                  <div className="bg-slate-950 border border-slate-800 rounded p-2.5 font-mono text-xs text-emerald-400 break-all select-all flex items-center justify-between gap-2">
                    <span>{constructedCommand}</span>
                    <button
                      onClick={() => copyToClipboard(constructedCommand, 'syntax')}
                      className="text-slate-400 hover:text-white p-1 shrink-0"
                      title="Copy Command"
                    >
                      {copiedKey === 'syntax' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>

                {/* Scan Execution Buttons */}
                <div className="flex items-center gap-2 pt-2">
                  {!isScanning ? (
                    <button
                      onClick={handleStartScan}
                      className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 bg-amber-400 hover:bg-amber-300 text-slate-950 font-semibold text-xs rounded transition-colors"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      {language === 'en' ? 'Execute Preset Scan' : 'স্ক্যান শুরু করুন'}
                    </button>
                  ) : (
                    <button
                      onClick={handleStopScan}
                      className="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 bg-rose-500 hover:bg-rose-400 text-white font-semibold text-xs rounded transition-colors"
                    >
                      <Square className="w-3.5 h-3.5 fill-current" />
                      {language === 'en' ? 'Cancel Execution' : 'স্ক্যান বাতিল'}
                    </button>
                  )}

                  <button
                    onClick={() => {
                      setScanOutput([]);
                      setAnalysisReport(null);
                    }}
                    className="p-2.5 border border-slate-800 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                    title="Clear Terminal"
                  >
                    <RefreshCw className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Tool Specs & Platform Info */}
              {selectedTool && (
                <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-3 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-white">{selectedTool.name}</span>
                    <a
                      href={selectedTool.official_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-amber-400 hover:underline flex items-center gap-1"
                    >
                      Official Docs <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                  <p className="text-slate-400 leading-relaxed">
                    {language === 'en' ? selectedTool.description : (selectedTool.bangla_description || selectedTool.description)}
                  </p>
                  <div className="flex flex-col gap-1.5 pt-2 border-t border-slate-800/80 text-slate-400 font-mono text-[11px]">
                    <div>Executable: <span className="text-white">{selectedTool.executable}</span></div>
                    <div>Installers: <span className="text-white">{selectedTool.installers.join(', ')}</span></div>
                    <div>Supported Platforms: <span className="text-white">{selectedTool.platforms.join(', ')}</span></div>
                  </div>
                </div>
              )}
            </div>

            {/* Right Terminal & AI Results Column (8 cols) */}
            <div className="lg:col-span-8 flex flex-col gap-5">
              {/* Terminal Console Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex flex-col">
                {/* Terminal Header */}
                <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                    <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                    <span className="ml-2 font-mono text-xs text-slate-400">
                      sunscan://terminal/{selectedTool?.id || 'live'}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
                    {isScanning && (
                      <span className="text-amber-400 flex items-center gap-1">
                        <span className="inline-block w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                        Elapsed: <strong className="tabular-nums">{scanElapsedTime}s</strong>
                      </span>
                    )}
                    {lastScanRecord && !isScanning && (
                      <span className="text-emerald-400 tabular-nums">
                        Exit: {lastScanRecord.exit_code}
                      </span>
                    )}
                  </div>
                </div>

                {/* Terminal Body */}
                <div className="p-4 bg-slate-950/90 font-mono text-xs text-slate-300 min-h-[360px] max-h-[500px] overflow-y-auto leading-relaxed select-text">
                  {scanOutput.length === 0 ? (
                    <div className="text-slate-600 italic py-12 text-center">
                      Ready to execute. Select a diagnostic tool preset and click 'Execute Preset Scan'.
                    </div>
                  ) : (
                    scanOutput.map((line, i) => (
                      <div
                        key={i}
                        className={`whitespace-pre-wrap ${
                          line.startsWith('[ERROR]')
                            ? 'text-rose-400 font-semibold'
                            : line.startsWith('[SUNSCAN]')
                            ? 'text-amber-400 font-medium'
                            : line.includes('open') && line.includes('/tcp')
                            ? 'text-emerald-400 font-semibold'
                            : line.startsWith('+') || line.startsWith('|')
                            ? 'text-cyan-300'
                            : 'text-slate-300'
                        }`}
                      >
                        {line}
                      </div>
                    ))
                  )}
                  <div ref={terminalEndRef} />
                </div>

                {/* Terminal Footer Bar */}
                <div className="bg-slate-900 px-4 py-2.5 border-t border-slate-800 flex items-center justify-between text-xs">
                  <div className="text-slate-400">
                    Lines: <strong className="text-white tabular-nums">{scanOutput.length}</strong>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleAnalyzeWithAI()}
                      disabled={isAnalyzing || scanOutput.length === 0}
                      className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white font-medium rounded flex items-center gap-1.5 transition-colors disabled:opacity-40"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      {isAnalyzing
                        ? (language === 'en' ? 'Analyzing with AI...' : 'এআই বিশ্লেষণ চলছে...')
                        : (language === 'en' ? 'Analyze Output with AI' : 'এআই দিয়ে বিশ্লেষণ করুন')}
                    </button>
                    {lastScanRecord && (
                      <button
                        onClick={() => downloadJSONReport(lastScanRecord)}
                        className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded flex items-center gap-1.5 transition-colors"
                      >
                        <Download className="w-3.5 h-3.5" />
                        {language === 'en' ? 'Export JSON' : 'জেসন এক্সপোর্ট'}
                      </button>
                    )}
                  </div>
                </div>
              </div>

              {/* AI Analysis Findings Card (Rendered when available) */}
              {analysisReport && (
                <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-cyan-400" />
                      <h3 className="text-sm font-semibold text-white">
                        {language === 'en' ? 'AI Security Posture Assessment' : 'এআই সিকিউরিটি পোস্টার অ্যাসেসমেন্ট'}
                      </h3>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-400">Risk Score:</span>
                      <span
                        className={`text-xs font-bold uppercase px-2 py-0.5 rounded ${
                          analysisReport.risk_score === 'high' || analysisReport.risk_score === 'critical'
                            ? 'bg-rose-500/20 text-rose-400 border border-rose-500/40'
                            : analysisReport.risk_score === 'medium'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                        }`}
                      >
                        {analysisReport.risk_score}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded border border-slate-800">
                    {analysisReport.summary}
                  </p>

                  {/* Findings breakdown */}
                  <div className="flex flex-col gap-3">
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      {language === 'en' ? 'Detailed Findings & Verifications' : 'সুনির্দিষ্ট ফাইন্ডিং ও যাচাইকরণ'} ({analysisReport.findings.length})
                    </h4>

                    {analysisReport.findings.length === 0 ? (
                      <div className="text-xs text-slate-500 italic p-3 text-center">
                        No critical vulnerabilities or misconfigurations discovered in this scan output.
                      </div>
                    ) : (
                      analysisReport.findings.map((f, idx) => (
                        <div
                          key={idx}
                          className="border border-slate-800 rounded-lg p-4 bg-slate-950/40 flex flex-col gap-2.5 text-xs"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-semibold text-white text-sm">{f.title}</span>
                            <div className="flex items-center gap-2">
                              <span
                                className={`text-[11px] font-mono px-2 py-0.5 rounded uppercase font-medium ${
                                  f.severity === 'critical' || f.severity === 'high'
                                    ? 'bg-rose-950 text-rose-300 border border-rose-800'
                                    : f.severity === 'medium'
                                    ? 'bg-amber-950 text-amber-300 border border-amber-800'
                                    : 'bg-slate-800 text-slate-300'
                                }`}
                              >
                                {f.severity}
                              </span>
                              {f.confidence && (
                                <span className="text-[11px] text-slate-500">
                                  conf: {f.confidence}
                                </span>
                              )}
                            </div>
                          </div>

                          <p className="text-slate-300 leading-relaxed">{f.explanation}</p>

                          {f.evidence && (
                            <div className="bg-slate-950 rounded p-2.5 font-mono text-[11px] text-amber-300/90 border border-slate-800/80 break-all">
                              <span className="text-slate-500 block mb-0.5 font-sans text-[10px] uppercase">Exact Output Evidence:</span>
                              {f.evidence}
                            </div>
                          )}

                          <div className="bg-emerald-950/20 border border-emerald-900/40 rounded p-2.5 text-emerald-300/90">
                            <span className="font-semibold block mb-0.5">Defensive Remediation:</span>
                            {f.recommendation}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: TOOL CATALOG EXPLORER */}
        {activeTab === 'catalog' && (
          <div className="flex flex-col gap-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white">
                  {language === 'en' ? 'Verified Cybersecurity Tool Catalog' : 'যাচাইকৃত সাইবার সিকিউরিটি টুল ক্যাটালগ'}
                </h2>
                <p className="text-xs text-slate-400">
                  Over 10+ core domains and 200+ empirically researched defensive security utilities.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Category:</span>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="bg-slate-900 border border-slate-800 text-xs text-white rounded px-3 py-1.5 focus:outline-none focus:border-amber-400"
                >
                  <option value="all">All Categories</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tools
                .filter((t) => selectedCategory === 'all' || t.category === selectedCategory)
                .map((tool) => (
                  <div
                    key={tool.id}
                    className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col justify-between gap-4 hover:border-slate-700 transition-colors"
                  >
                    <div className="flex flex-col gap-2">
                      <div className="flex items-center justify-between">
                        <span className="text-base font-bold text-white">{tool.name}</span>
                        <span className="text-xs font-mono text-slate-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                          {tool.category}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {language === 'en' ? tool.description : (tool.bangla_description || tool.description)}
                      </p>
                    </div>

                    <div className="flex flex-col gap-2 border-t border-slate-800/80 pt-3 text-xs">
                      <div className="flex items-center justify-between text-slate-400">
                        <span>Presets Available:</span>
                        <strong className="text-white tabular-nums">{tool.commands?.length || 0}</strong>
                      </div>
                      <div className="flex items-center justify-between text-slate-400">
                        <span>Root Privilege:</span>
                        <strong className="text-white">{tool.requires_root ? 'Required' : 'Rootless Safe'}</strong>
                      </div>
                      <div className="flex items-center justify-between text-slate-400">
                        <span>Installers:</span>
                        <span className="font-mono text-[11px] text-amber-400">{tool.installers.join(', ')}</span>
                      </div>

                      <div className="flex items-center justify-between pt-2">
                        <a
                          href={tool.repository}
                          target="_blank"
                          rel="noreferrer"
                          className="text-slate-400 hover:text-white flex items-center gap-1 text-[11px]"
                        >
                          Repository <ExternalLink className="w-3 h-3" />
                        </a>
                        <button
                          onClick={() => {
                            setSelectedToolId(tool.id);
                            if (tool.commands?.length > 0) setSelectedCommandId(tool.commands[0].id);
                            setActiveTab('workbench');
                          }}
                          className="px-3 py-1 bg-amber-400 hover:bg-amber-300 text-slate-950 font-semibold text-xs rounded transition-colors"
                        >
                          Open in Workbench
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* TAB 3: STANDALONE AI ANALYZER */}
        {activeTab === 'analyzer' && (
          <div className="flex flex-col gap-6">
            <div>
              <h2 className="text-lg font-bold text-white">
                {language === 'en' ? 'AI Scan Output Analyzer' : 'এআই স্ক্যান আউটপুট অ্যানালাইজার'}
              </h2>
              <p className="text-xs text-slate-400">
                Paste raw scanner logs (Nmap, Nikto, Feroxbuster, testssl.sh, Subfinder) to extract structured findings and remediation steps.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
              {/* Input text box */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-white uppercase tracking-wider">
                    {language === 'en' ? 'Raw Scan Output / Terminal Log' : 'কাঁচা স্ক্যান আউটপুট পেস্ট করুন'}
                  </label>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => {
                        setManualOutputInput(
                          `Starting Nmap 7.95 ( https://nmap.org )\nNmap scan report for ${targetInput}\nPORT     STATE SERVICE VERSION\n22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu\n80/tcp   open  http    Apache httpd 2.4.52\n443/tcp  open  ssl/http Apache httpd 2.4.52\nNmap done: 1 IP address scanned.`
                        );
                      }}
                      className="text-[11px] text-amber-400 hover:underline"
                    >
                      Load Sample Output
                    </button>
                  </div>
                </div>

                <textarea
                  rows={14}
                  value={manualOutputInput}
                  onChange={(e) => setManualOutputInput(e.target.value)}
                  placeholder="Paste raw scanner output here..."
                  className="w-full bg-slate-950 border border-slate-800 rounded p-3 text-xs font-mono text-slate-200 focus:outline-none focus:border-amber-400 leading-relaxed"
                />

                <div className="flex items-center justify-between pt-2">
                  <span className="text-xs text-slate-500">
                    Character count: {manualOutputInput.length}
                  </span>
                  <button
                    onClick={() => handleAnalyzeWithAI(manualOutputInput)}
                    disabled={isAnalyzing || !manualOutputInput.trim()}
                    className="px-4 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-semibold text-xs rounded transition-colors disabled:opacity-40 flex items-center gap-1.5"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    {isAnalyzing
                      ? (language === 'en' ? 'Generating Analysis...' : 'বিশ্লেষণ তৈরি হচ্ছে...')
                      : (language === 'en' ? 'Generate AI Security Report' : 'এআই সিকিউরিটি রিপোর্ট তৈরি করুন')}
                  </button>
                </div>
              </div>

              {/* Output analysis view */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4">
                <h3 className="text-xs font-semibold text-white uppercase tracking-wider">
                  {language === 'en' ? 'Structured Analysis Result' : 'বিশ্লেষণের ফলাফল'}
                </h3>

                {!analysisReport ? (
                  <div className="text-center py-20 text-slate-600 italic text-xs">
                    Paste scanner output and click 'Generate AI Security Report' to see findings here.
                  </div>
                ) : (
                  <div className="flex flex-col gap-4">
                    <div className="p-3 bg-slate-950 rounded border border-slate-800 text-xs text-slate-300">
                      <strong className="text-white block mb-1">Executive Summary:</strong>
                      {analysisReport.summary}
                    </div>

                    <div className="flex flex-col gap-3">
                      {analysisReport.findings.map((f, i) => (
                        <div key={i} className="p-3.5 rounded bg-slate-950 border border-slate-800 text-xs flex flex-col gap-2">
                          <div className="flex items-center justify-between">
                            <span className="font-semibold text-white">{f.title}</span>
                            <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-amber-300">
                              {f.severity}
                            </span>
                          </div>
                          <p className="text-slate-300">{f.explanation}</p>
                          {f.evidence && (
                            <div className="p-2 bg-slate-900 rounded font-mono text-[11px] text-slate-400 border border-slate-800/80">
                              {f.evidence}
                            </div>
                          )}
                          <div className="text-emerald-400 font-medium pt-1">
                            Recommendation: {f.recommendation}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: REPORTS & SCAN HISTORY */}
        {activeTab === 'reports' && (
          <div className="flex flex-col gap-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-white">
                  {language === 'en' ? 'Scan History & Reports' : 'স্ক্যান হিস্ট্রি ও রিপোর্টসমূহ'}
                </h2>
                <p className="text-xs text-slate-400">
                  Archived execution records and security audit logs stored on local storage.
                </p>
              </div>
              <button
                onClick={fetchReports}
                className="px-3 py-1.5 border border-slate-800 rounded text-xs text-slate-300 hover:text-white hover:bg-slate-800 flex items-center gap-1.5 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                {language === 'en' ? 'Refresh' : 'রিফ্রেশ'}
              </button>
            </div>

            {reportsList.length === 0 ? (
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-12 text-center text-slate-500 italic text-xs">
                No past scan reports found. Run a diagnostic scan in the Workbench to generate records.
              </div>
            ) : (
              <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950 border-b border-slate-800 text-slate-400 font-medium">
                    <tr>
                      <th className="p-3.5 font-mono">Scan ID</th>
                      <th className="p-3.5">Tool</th>
                      <th className="p-3.5">Target</th>
                      <th className="p-3.5">Status</th>
                      <th className="p-3.5">Timestamp</th>
                      <th className="p-3.5 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono">
                    {reportsList.map((r) => (
                      <tr key={r.scan_id} className="hover:bg-slate-800/30 transition-colors">
                        <td className="p-3.5 font-semibold text-amber-400">{r.scan_id}</td>
                        <td className="p-3.5 font-sans font-medium text-white">{r.tool_name || r.tool_id}</td>
                        <td className="p-3.5 text-slate-300">{r.target}</td>
                        <td className="p-3.5 font-sans">
                          <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                            r.status === 'completed' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/80' : 'bg-rose-950 text-rose-400'
                          }`}>
                            {r.status}
                          </span>
                        </td>
                        <td className="p-3.5 text-slate-400 text-[11px]">{r.start_time?.substring(0, 19).replace('T', ' ')}</td>
                        <td className="p-3.5 text-right font-sans">
                          <button
                            onClick={() => downloadJSONReport(r)}
                            className="px-2.5 py-1 text-slate-300 hover:text-white border border-slate-700 rounded text-xs hover:bg-slate-800 transition-colors"
                          >
                            Download JSON
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* TAB 5: DIAGNOSTICS */}
        {activeTab === 'diagnostics' && (
          <div className="flex flex-col gap-6">
            <div>
              <h2 className="text-lg font-bold text-white">
                {language === 'en' ? 'System Environment & Tool Health' : 'সিস্টেম পরিবেশ ও টুল পর্যবেক্ষণ'}
              </h2>
              <p className="text-xs text-slate-400">
                Host OS platform, package manager detection, Python runtime, and individual security scanner availability.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
              {/* Host telemetry card */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4 text-xs">
                <h3 className="font-semibold text-white uppercase tracking-wider">
                  Host Platform Details
                </h3>
                <div className="flex flex-col gap-2.5 divide-y divide-slate-800/80 font-mono">
                  <div className="flex justify-between py-1.5 text-slate-300">
                    <span className="font-sans text-slate-400">Operating System:</span>
                    <span className="font-bold text-white">{diagnosticsData?.system || 'Linux'}</span>
                  </div>
                  <div className="flex justify-between py-1.5 text-slate-300">
                    <span className="font-sans text-slate-400">Architecture:</span>
                    <span className="text-white">{diagnosticsData?.arch || 'x86_64'}</span>
                  </div>
                  <div className="flex justify-between py-1.5 text-slate-300">
                    <span className="font-sans text-slate-400">Node Runtime:</span>
                    <span className="text-white">{diagnosticsData?.nodeVersion || 'v20+'}</span>
                  </div>
                  <div className="flex justify-between py-1.5 text-slate-300">
                    <span className="font-sans text-slate-400">Root Privileges:</span>
                    <span className="text-white">{diagnosticsData?.isRoot ? 'Elevated (UID 0)' : 'Unprivileged User'}</span>
                  </div>
                  <div className="flex justify-between py-1.5 text-slate-300">
                    <span className="font-sans text-slate-400">Package Manager:</span>
                    <span className="text-emerald-400 font-semibold">apt / pkg</span>
                  </div>
                </div>
              </div>

              {/* Tool installation status card */}
              <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 flex flex-col gap-4 text-xs">
                <h3 className="font-semibold text-white uppercase tracking-wider">
                  Tool Installation Status
                </h3>
                <div className="max-h-[380px] overflow-y-auto flex flex-col gap-2 pr-1">
                  {(diagnosticsData?.tools || tools).map((t: any) => (
                    <div
                      key={t.id}
                      className="flex items-center justify-between p-2.5 bg-slate-950 rounded border border-slate-800/80"
                    >
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-white">{t.name}</span>
                        <span className="font-mono text-[11px] text-slate-500">({t.executable})</span>
                      </div>
                      <span
                        className={`text-[11px] px-2 py-0.5 rounded font-mono font-medium ${
                          t.installed
                            ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                            : 'bg-slate-800 text-slate-400'
                        }`}
                      >
                        {t.installed ? 'INSTALLED' : 'OPTIONAL (NOT INSTALLED)'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* TARGET AUTHORIZATION MODAL */}
      {showAuthModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 max-w-lg w-full rounded-lg p-6 flex flex-col gap-4 shadow-2xl">
            <div className="flex items-center gap-3 text-amber-400">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="text-base font-bold text-white">
                Authorized Testing & Ethics Confirmation
              </h3>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              SUNSCAN is designed strictly for defensive cybersecurity auditing, education, and authorized diagnostic posture review.
            </p>

            <div className="bg-slate-950 p-3.5 rounded border border-slate-800 text-xs text-slate-400 leading-relaxed flex flex-col gap-2">
              <div className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>I confirm that I own this target or have documented, signed permission to test this asset.</span>
              </div>
              <div className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>I understand scans must follow non-disruptive, rate-limited procedures without causing denial of service.</span>
              </div>
              <div className="flex items-start gap-2">
                <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>SUNSCAN enforces unprivileged presets and does not execute weaponized exploits.</span>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setShowAuthModal(false)}
                className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  setAuthConfirmed(true);
                  setShowAuthModal(false);
                  handleStartScan();
                }}
                className="px-4 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold text-xs rounded transition-colors"
              >
                I Confirm & Authorize Scan
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SETTINGS MODAL */}
      {showSettingsModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 max-w-md w-full rounded-lg p-6 flex flex-col gap-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Settings className="w-4 h-4 text-amber-400" />
                SUNSCAN Settings & AI Providers
              </h3>
              <button
                onClick={() => setShowSettingsModal(false)}
                className="text-slate-400 hover:text-white text-xs"
              >
                ✕
              </button>
            </div>

            <div className="flex flex-col gap-3 text-xs">
              <div className="flex flex-col gap-1.5">
                <label className="text-slate-300 font-medium">OpenRouter API Key (Optional)</label>
                <input
                  type="password"
                  value={openRouterKey}
                  onChange={(e) => setOpenRouterKey(e.target.value)}
                  placeholder="sk-or-v1-..."
                  className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white font-mono text-xs focus:outline-none focus:border-amber-400"
                />
                <span className="text-[11px] text-slate-500">
                  If left blank, SUNSCAN uses server-side Google Gemini 3.8 Flash automatically.
                </span>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-slate-300 font-medium">OpenRouter Model</label>
                <select
                  value={openRouterModel}
                  onChange={(e) => setOpenRouterModel(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded px-3 py-2 text-white text-xs focus:outline-none focus:border-amber-400"
                >
                  <option value="google/gemini-2.0-flash-001">Google Gemini 2.0 Flash</option>
                  <option value="anthropic/claude-3.5-haiku">Anthropic Claude 3.5 Haiku</option>
                  <option value="meta-llama/llama-3.3-70b-instruct">Meta Llama 3.3 70B Instruct</option>
                </select>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-slate-300 font-medium">Preferred Reporting Language</label>
                <div className="flex items-center gap-3 pt-1">
                  <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
                    <input
                      type="radio"
                      name="lang"
                      checked={language === 'en'}
                      onChange={() => setLanguage('en')}
                    />
                    English
                  </label>
                  <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
                    <input
                      type="radio"
                      name="lang"
                      checked={language === 'bn'}
                      onChange={() => setLanguage('bn')}
                    />
                    বাংলা (Bengali)
                  </label>
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setShowSettingsModal(false)}
                className="px-4 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold text-xs rounded transition-colors"
              >
                Save Settings
              </button>
            </div>
          </div>
        </div>
      )}

      {/* FOOTER */}
      <footer className="border-t border-slate-800/80 bg-slate-950 px-6 py-4 mt-auto text-xs text-slate-500 flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          SUNSCAN v1.0.0 · A <strong>CodeSun</strong> Open-Source Cybersecurity Initiative · MIT License
        </div>
        <div className="flex items-center gap-5">
          <span className="font-mono text-slate-600">npm i -g sunscan-cli</span>
          <span aria-hidden="true" className="text-slate-700">·</span>
          <span>Defensive Auditing</span>
          <span aria-hidden="true" className="text-slate-700">·</span>
          <span>Ethical Verification Only</span>
        </div>
      </footer>
    </div>
  );
}
