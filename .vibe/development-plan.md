# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore

### Phase Entrance Criteria:
- [x] Vorherige Komponenten sind abgeschlossen (KrokiClient, Config, CLI)
- [x] ADR-002 (Agent Self-Iteration) verstanden
- [x] Runtime View Scenario 1 analysiert (kompletter Feedback-Loop)
- [x] Building Block View Level 2 studiert (Orchestrator-Komponenten)

### Tasks
- [x] ADR-002 lesen: Agent iteriert autonom mit eigenem LLM-Client
- [x] Runtime View analysieren: Initial → Validate → Analyze → Refine → Approve
- [x] Quality Scenarios: 95% Syntax-Fehler in 2 Iterations, < 60s total
- [x] Limits verstehen: MAX_ITERATIONS=5, MAX_TIME_SECONDS=60
- [x] Dependencies identifizieren: LLMClient, PromptBuilder, Validator, Analyzer, Limiter, Writer
- [x] MVP-Scope definieren: Iteration-Loop mit KrokiClient (bereits fertig ✓)

### Completed
- [x] ADR-002: Autonome Iteration, eigener LLM-Client, < 3k parent tokens
- [x] Runtime View: 2-Iterations-Beispiel mit Validator + Analyzer
- [x] Limits: max_iterations=5, max_time_seconds=60 aus Settings
- [x] Dependencies: KrokiClient vorhanden ✓, LLMClient/Analyzer/Writer fehlen
- [x] MVP-Strategie: Start mit Validation-Loop (KrokiClient), später Analyzer + Writer

## Red

### Phase Entrance Criteria:
- [x] Exploration ist abgeschlossen und Anforderungen sind dokumentiert
- [x] Architektur-Entscheidungen aus arc42-Dokumentation sind verstanden
- [x] Bestehende Patterns und Konventionen sind erfasst
- [x] Es ist klar, welche Funktionalität als nächstes implementiert werden soll

### Tasks
- [x] **Orchestrator (Zyklus 1):** Tests für Iteration-Limits schreiben
- [x] Test 1: `test_orchestrator_respects_max_iterations` - Iteration counting + limit
- [x] Test 2: `test_orchestrator_respects_time_limit` - Time tracking + timeout
- [x] Tests validieren Metadata: iterations_used, elapsed_seconds, stopped_reason
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 2 Tests in tests/unit/test_orchestrator.py geschrieben
- [x] Test 1 validiert: iterations_used <= max_iterations (aus Settings)
- [x] Test 2 validiert: elapsed_seconds <= max_time_seconds + 1s grace
- [x] Beide Tests validieren stopped_reason (max_iterations | max_time | success)
- [x] Tests schlagen fehl: Missing iterations_used/elapsed_seconds metadata (erwartet) ✅

## Green

### Phase Entrance Criteria:
- [x] Ein spezifischer, fokussierter Test wurde geschrieben
- [x] Der Test schlägt fehl (RED) aus dem richtigen Grund
- [x] Test validiert tatsächlich die erwartete Funktionalität
- [x] Test-Typ (Unit/Integration) wurde mit User abgestimmt

### Tasks
- [x] **CLI Basis (Zyklus 1):** Click CLI mit --help implementieren
- [x] @click.group() als Entry Point mit Version
- [x] @click.command() für create mit Description
- [x] Options: --type, --output, --format
- [x] Tests ausführen und grün machen
- [x] **CLI Basis (Zyklus 2):** create command mit Orchestrator-Integration
- [x] Minimal Orchestrator-Klasse mit execute() erstellen
- [x] Settings + Orchestrator in CLI importieren
- [x] create() ruft orchestrator.execute() auf
- [x] Tests ausführen und grün machen

### Completed
- [x] CLI Basis Zyklus 1: --help (100% Coverage) ✅
- [x] CLI Basis Zyklus 2: Orchestrator-Stub in src/diag_agent/agent/orchestrator.py
- [x] CLI Basis Zyklus 2: CLI integriert Settings + Orchestrator
- [x] CLI Basis Zyklus 2: create() ruft orchestrator.execute() auf
- [x] CLI Tests passed! ✅ (CLI: 100% Coverage)
- [x] **Orchestrator Zyklus 1:** Iteration-Loop mit while-Schleife
- [x] **Orchestrator Zyklus 1:** Zeit-Tracking (start_time, elapsed)
- [x] **Orchestrator Zyklus 1:** Limits aus Settings (max_iterations, max_time_seconds)
- [x] **Orchestrator Zyklus 1:** stopped_reason Logic (3 Zustände)
- [x] Orchestrator Tests passed! ✅ (87% Coverage)
- [x] **Zyklus 2:** Error-Message mit status code + diagram type
- [x] Beide Tests passed! ✅ (100% Coverage)

## Refactor

### Phase Entrance Criteria:
- [x] Der Test ist grün (PASS)
- [x] Implementation ist vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [x] Die Lösung adressiert das eigentliche Problem

### Tasks
- [x] **CLI Basis (Zyklus 1):** Code Review durchführen
- [x] Click decorators geprüft: Korrekt verwendet ✓
- [x] Docstrings vollständig mit Examples ✓
- [x] Context-Efficiency validiert: Help output < 500 tokens ✓
- [x] Keine Refactorings nötig - Code ist clean
- [x] **CLI Basis (Zyklus 2):** Code Review durchführen
- [x] Built-in override identifiziert: `type` Parameter
- [x] Refactoring: `type` → `diagram_type` (konsistent mit Orchestrator)
- [x] Tests validieren (alle grün ✓)

### Completed
- [x] Zyklus 1: Code Review - keine Änderungen nötig ✅
- [x] Zyklus 2: Built-in override behoben (type → diagram_type)
- [x] Zyklus 2: Konsistenz mit Orchestrator.execute() hergestellt
- [x] Alle Tests passed ✅ (CLI: 100% Coverage)
- [x] CLI Basis Zyklus 2 abgeschlossen ✅ (create mit Orchestrator)

## Key Decisions

### Architektur-Entscheidungen (aus ADRs)
- **ADR-001**: Bash-Tool mit `--help` ist primär, MCP optional → Context-Effizienz
- **ADR-002**: Agent iteriert selbständig mit eigenem LLM-Client → Autonomie
- **ADR-003**: Local-First (Kroki Fat-JAR), kroki.io nur mit Consent → Privacy
- **ADR-005**: LiteLLM für Provider-Abstraction → 100+ Modelle unterstützt
- **ADR-006**: Docker mit gebundeltem Kroki (Fat-JAR) → Einfache Installation
- **ADR-008**: Click als CLI Framework → Rich UX, LLM-kompatibel
- **ADR-009**: uv/uvx als Package Management (ACCEPTED) → 5-10x schneller, modern (PEP 723)

### Tech Stack
- **Python**: 3.10+ (bestehende Expertise)
- **Package Management**: uv/uvx (PEP 723, einzige empfohlene Methode)
- **CLI**: Click (intuitive commands, gute Help-Ausgabe)
- **LLM**: LiteLLM (Provider-agnostisch)
- **MCP**: FastMCP (Standard-Protokoll)
- **Rendering**: Kroki (20+ Diagramm-Typen)
- **Config**: python-dotenv, PyYAML
- **HTTP**: requests/httpx
- **Testing**: pytest (Unit- und Integrationstests)

### Qualitätsziele (Priorität)
1. **Context Efficiency**: < 3k tokens pro Diagramm-Request
2. **Ease of Installation**: < 2 Min bis zum ersten Diagramm (mit uvx)
3. **Privacy & Security**: Local-First, kein Remote ohne Consent
4. **Autonomy**: Agent iteriert ohne Parent-LLM Intervention
5. **Extensibility**: Alle Kroki-Typen, einfacher Provider-Wechsel

### Test-Strategie (RED-Phase)
- **Test-Typ**: Unit-Test mit HTTP-Mock (pytest + unittest.mock)
- **TDD-Zyklen**:
  - Zyklus 1: Happy-Path (`test_render_diagram_success`) - PlantUML → PNG
  - Zyklus 2: Error-Handling (`test_render_diagram_http_error`) - HTTP 500 → KrokiRenderError
- **Design**: Generisches Interface + Custom Exception für klare Error-Messages

## Notes

### ADR-009 Accepted (2025-12-15)
**Decision**: Vollständige Migration zu uv/uvx als einziges Package Management Tool
- README.md vollständig auf uv umgestellt (kein pip-Fallback mehr)
- Installation, Quick Start, Development, und Usage Examples zeigen nur noch uv/uvx
- Qualitätsziel "Ease of Installation" adressiert: uvx ermöglicht Zero-Install-Execution

### Config Management - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 1 TDD-Zyklus komplett (RED→GREEN→REFACTOR)
- ✅ Settings-Klasse mit ENV + .env Support
- ✅ Graceful Error-Handling für ungültige Integer-Werte
- ✅ 3 Tests, 100% Coverage
- ✅ Production-ready: python-dotenv, type-safe

**Implementiert:**
- 7 Config-Optionen (LLM, Kroki, Agent, Logging)
- ENV var precedence: ENV > .env > defaults
- Helper-Methode `_get_int_env()` für robuste Type Conversion

### CLI Basis - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 2 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Zyklus 1: `--help` output mit Click framework
- ✅ Zyklus 2: `create` command mit Orchestrator + Settings integration
- ✅ 100% CLI Coverage, 2 Tests passing
- ✅ Refactoring: `type` → `diagram_type` (built-in override fix)

**Implementiert:**
- Click @click.group() mit version 0.1.0
- create command mit --type, --output, --format options
- Settings + Orchestrator integration
- Minimal Orchestrator-Stub für Tests

### Orchestrator - IN ARBEIT 🚧 (2025-12-15)
**Status**: EXPLORE phase abgeschlossen, RED phase startet

**TDD-Strategie:**
- **Test-Typ**: Unit-Test mit Mocks für LLMClient, PromptBuilder, Analyzer
- **TDD-Zyklen geplant**:
  - Zyklus 1: Iteration-Loop mit KrokiClient (Validation nur)
  - Zyklus 2: Iteration Limits (max_iterations, max_time_seconds)
  - Zyklus 3 (später): LLMClient + PromptBuilder integration
  - Zyklus 4 (später): Design Analyzer (Vision) integration

**Orchestrator-Anforderungen (aus arc42):**
- Autonome Iteration ohne Parent-LLM (ADR-002)
- Feedback-Loop: Prompt → LLM → Validate → Analyze → Refine
- Limits: max_iterations=5, max_time_seconds=60 (aus Settings)
- Dependencies: KrokiClient ✓, LLMClient ⏳, Analyzer ⏳, Writer ⏳

**Design-Entscheidungen:**
- MVP-Scope: Start mit Validation-Loop (KrokiClient bereits fertig)
- Later: Integration mit LLMClient, PromptBuilder, Analyzer
- Iteration state management: count + time tracking

### KrokiClient - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 2 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Happy-Path: render_diagram() mit HTTP POST
- ✅ Error-Handling: KrokiRenderError mit Context
- ✅ 100% Test Coverage
- ✅ Production-ready: Clean Code, keine TODOs

### MVP-Strategie: Bottom-Up mit Kroki Client
**Erste Komponente: Kroki Client** (`src/diag_agent/kroki/client.py`) ✅
- Klare Schnittstelle: HTTP POST → Kroki → PNG/SVG Response
- Keine komplexen Abhängigkeiten
- Gut testbar (Unit + Integration mit Mock/Real Kroki)
- Foundation für Agent Core

**Nächste Schritte nach Kroki Client:**
1. Config Management (Settings laden)
2. CLI Basis (Click command für `create`)
3. LLM Client (LiteLLM wrapper)
4. Agent Core (Orchestrator mit Feedback-Loop)
5. MCP Server (optional)

### Projekt-Struktur (src-Layout)
```
diag-agent/
├── src/
│   └── diag_agent/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: python -m diag_agent
│       ├── cli/                # Click CLI commands
│       │   ├── __init__.py
│       │   └── commands.py
│       ├── agent/              # Agent Core
│       │   ├── __init__.py
│       │   ├── orchestrator.py # Main feedback loop
│       │   ├── prompt_builder.py
│       │   ├── validator.py    # Syntax validation
│       │   ├── analyzer.py     # Design analysis (vision)
│       │   └── limiter.py      # Iteration/time limits
│       ├── llm/                # LLM Client
│       │   ├── __init__.py
│       │   └── client.py       # LiteLLM wrapper
│       ├── kroki/              # Kroki Manager
│       │   ├── __init__.py
│       │   ├── client.py       # HTTP client
│       │   └── manager.py      # Lifecycle, health checks
│       ├── config/             # Configuration
│       │   ├── __init__.py
│       │   └── settings.py     # Config precedence
│       ├── mcp/                # MCP Server (optional)
│       │   ├── __init__.py
│       │   └── server.py       # FastMCP implementation
│       └── utils/              # Utilities
│           ├── __init__.py
│           └── logging.py
├── tests/
│   ├── unit/
│   │   └── test_kroki_client.py
│   └── integration/
│       └── test_feedback_loop.py
├── pyproject.toml
├── README.md
└── .env.example
```

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
