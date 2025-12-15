# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore

### Phase Entrance Criteria:
- [x] LLM Client Cycle 1 abgeschlossen (generate mit LiteLLM)
- [x] Orchestrator Cycle 1 vorhanden (Iteration-Loop mit Limits)
- [x] Runtime View Scenario 1 dokumentiert (Orch → LLM → Validator)
- [x] Bestehende Tests verstanden (max_iterations, max_time)

### Tasks
- [x] Aktuellen Orchestrator-Code analysieren: Hardcoded diagram_source
- [x] Runtime View studieren: Orch → LLM.generate(prompt) → PlantUML source
- [x] LLMClient-Interface verstehen: generate(prompt) → str
- [x] Bestehende Tests prüfen: Mock-basiert, können erweitert werden
- [x] MVP-Scope definieren: LLMClient-Integration, simple Prompt-Konstruktion
- [x] Dependencies: LLMClient ✓, KrokiClient ✓ (noch nicht genutzt)

### Completed
- [x] Orchestrator TODO-Kommentar: "Call LLMClient to generate diagram source"
- [x] Runtime View: Orch → Prompt Builder → LLM.generate() → source
- [x] LLMClient-API: generate(prompt: str) → str (bereits fertig ✓)
- [x] Bestehende Tests: 2 Tests für Iteration-Limits, beide grün
- [x] MVP-Strategie: Simple Prompt (f"Generate {type}: {description}"), LLMClient-Call
- [x] Validation-Loop verschoben auf Cycle 3 (KrokiClient-Integration)

## Red

### Phase Entrance Criteria:
- [x] Exploration ist abgeschlossen und Anforderungen sind dokumentiert
- [x] Architektur-Entscheidungen aus arc42-Dokumentation sind verstanden
- [x] Bestehende Patterns und Konventionen sind erfasst
- [x] Es ist klar, welche Funktionalität als nächstes implementiert werden soll

### Tasks
- [x] **Orchestrator (Zyklus 2):** Test für LLMClient-Integration schreiben
- [x] Test: `test_orchestrator_uses_llm_client_for_generation`
- [x] Test validiert: LLMClient.generate() Call mit Prompt (description + type)
- [x] Test validiert: Result enthält LLM-Output (nicht hardcoded)
- [x] Test ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] Test in tests/unit/test_orchestrator.py hinzugefügt
- [x] Test validiert: Orchestrator → LLMClient.generate(prompt)
- [x] Test validiert: Prompt enthält description + diagram_type
- [x] Test validiert: diagram_source vom LLM (nicht "' Generated diagram")
- [x] Test schlägt fehl: AttributeError (LLMClient nicht importiert) ✅

## Green

### Phase Entrance Criteria:
- [x] Ein spezifischer, fokussierter Test wurde geschrieben
- [x] Der Test schlägt fehl (RED) aus dem richtigen Grund
- [x] Test validiert tatsächlich die erwartete Funktionalität
- [x] Test-Typ (Unit/Integration) wurde mit User abgestimmt

### Tasks
- [x] **Orchestrator (Zyklus 2):** LLMClient-Integration implementieren
- [x] LLMClient import auf Modul-Ebene hinzufügen
- [x] LLMClient im __init__ instantiieren
- [x] Prompt bauen: f"Generate a {diagram_type} diagram: {description}"
- [x] llm_client.generate(prompt) aufrufen
- [x] diagram_source vom LLM verwenden (nicht hardcoded)
- [x] Alte Tests anpassen: LLMClient mocken
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] LLMClient importiert in orchestrator.py ✅
- [x] self.llm_client = LLMClient(settings) in __init__ ✅
- [x] Simple Prompt: f"Generate a {diagram_type} diagram: {description}" ✅
- [x] diagram_source = self.llm_client.generate(prompt) ✅
- [x] Alte Tests gefixt: LLMClient-Mock hinzugefügt ✅
- [x] 3 Tests passed! ✅ (89% Coverage für Orchestrator)

## Refactor

### Phase Entrance Criteria:
- [x] Der Test ist grün (PASS)
- [x] Implementation ist vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [x] Die Lösung adressiert das eigentliche Problem

### Tasks
- [x] **Orchestrator (Zyklus 2):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft: LLMClient integration korrekt ✓
- [x] Prompt-Konstruktion validiert: Simple MVP-Format okay ✓
- [x] Pattern-Konsistenz: Analog zu KrokiClient ✓
- [x] Keine Refactorings nötig - Code ist clean

### Completed
- [x] Code Review durchgeführt: Keine Änderungen nötig ✅
- [x] Pattern konsistent (Dependency Injection, Settings-based config)
- [x] Docstrings vollständig, Type hints angemessen
- [x] Tests passed ✅ (89% Coverage für Orchestrator)
- [x] Orchestrator Zyklus 2 abgeschlossen ✅ (LLMClient-Integration)

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

### LLM Client - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 1 TDD-Zyklus komplett (RED→GREEN→REFACTOR)

**EXPLORE-Erkenntnisse:**
- **ADR-005**: LiteLLM für Provider-Abstraction → 100+ Modelle
- **Building Block View L2**: LLM Client = LiteLLM wrapper mit retry + error handling
- **Runtime View**: `generate(prompt)` → Diagramm-Source, später `vision_analyze(png)`
- **Bestehende Patterns**: KrokiClient-Struktur als Template (Custom Exception + Client-Klasse)
- **Settings-Integration**: llm_provider + llm_model (bereits in Settings ✓)

**MVP-Scope (erster TDD-Zyklus):**
- ✅ Text-Generierung (keine Vision)
- ✅ LiteLLM-Integration mit completion()
- ✅ Settings-basierte Provider/Model-Konfiguration
- ✅ Error-Handling für LLM API Errors
- ⏸️ Vision-Modus (später)
- ⏸️ Retry-Logic (später)
- ⏸️ Token-Counting (später)

**Dependencies:**
- Settings ✓ (llm_provider, llm_model)
- litellm package (muss installiert werden)
- httpx (bereits für KrokiClient installiert)

**Design-Entscheidungen:**
- Analog zu KrokiClient: Custom Exception (LLMGenerationError) + Client-Klasse
- Main method: `generate(prompt: str) -> str`
- LiteLLM completion() API nutzen
- Settings für Provider/Model statt hardcoded values

### Orchestrator - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 2 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Zyklus 1: Iteration-Loop mit max_iterations + max_time_seconds
- ✅ Zyklus 2: LLMClient-Integration für echte Generierung
- ✅ 3 Tests, 89% Coverage
- ✅ stopped_reason Logic (max_iterations | max_time | success)

**Implementiert:**
- Iteration-Loop mit while iterations_used < max_iterations
- Zeit-Tracking mit time.time() (start + elapsed)
- Limits aus Settings (max_iterations=5, max_time_seconds=60)
- Metadata: iterations_used, elapsed_seconds, stopped_reason
- LLMClient-Integration: self.llm_client = LLMClient(settings)
- Simple Prompt-Konstruktion: f"Generate a {diagram_type} diagram: {description}"
- LLM-Aufruf: diagram_source = self.llm_client.generate(prompt)

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
