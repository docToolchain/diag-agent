# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore

### Phase Entrance Criteria:
- [x] Orchestrator Cycle 2 abgeschlossen (LLMClient-Integration)
- [x] KrokiClient vorhanden (render_diagram mit Error-Handling)
- [x] Runtime View Scenario 2 dokumentiert (Orch → Validator → Error → LLM fix)
- [x] Bestehende Tests verstanden (3 Orchestrator-Tests, 2 Kroki-Tests)

### Tasks
- [x] **Orchestrator (Zyklus 3):** KrokiClient-Integration analysieren
- [x] KrokiClient API verstehen: render_diagram(source, type, format) → bytes or KrokiRenderError
- [x] Error-Message Format: "Kroki rendering failed for diagram type '{type}': HTTP {status} - {text}"
- [x] Runtime View Scenario 2 studieren: Validation-Loop mit LLM-Retry
- [x] MVP-Scope definieren: Validation ohne Analyzer (nur Syntax, kein Design)
- [x] Test-Strategie: Success-Case (LLM → Kroki ✅) + Error-Case (LLM → Kroki ❌ → Retry)

### Completed
- [x] KrokiClient-API: render_diagram() wirft KrokiRenderError bei Syntax-Error ✓
- [x] Error enthält: Status Code + Response Text (Kroki Error-Message)
- [x] Runtime View: Orch → Validator → Error → LLM fix(source, error) → Validator
- [x] MVP ohne separaten Validator: KrokiClient direkt im Orchestrator
- [x] 2 Test-Szenarien: (1) Success path, (2) Error → Retry → Success
- [x] Dependencies: KrokiClient ✓, LLMClient ✓, beide mit Error-Handling

## Red

### Phase Entrance Criteria:
- [x] Exploration ist abgeschlossen und Anforderungen sind dokumentiert
- [x] KrokiClient API verstanden (render_diagram + KrokiRenderError)
- [x] Test-Strategie definiert (2 Tests: Success + Error-Retry)
- [x] Es ist klar, welche Funktionalität als nächstes implementiert werden soll

### Tasks
- [x] **Orchestrator (Zyklus 3):** Tests für KrokiClient-Validation schreiben
- [x] Test 1: `test_orchestrator_validates_with_kroki_success`
- [x] Test validiert: KrokiClient.render_diagram() Call für Syntax-Check
- [x] Test validiert: Success-Path (1 Iteration, kein Retry)
- [x] Test 2: `test_orchestrator_retries_on_kroki_validation_error`
- [x] Test validiert: Error → Retry mit Error-Message im Prompt
- [x] Test validiert: 2 Iterationen, 2. erfolgreich
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 2 Tests in tests/unit/test_orchestrator.py hinzugefügt
- [x] Test 1: Success-Path (LLM → Kroki ✅ → Done)
- [x] Test 2: Error-Retry (LLM → Kroki ❌ → LLM fix → Kroki ✅)
- [x] Mocks: LLMClient + KrokiClient (wie in Cycle 1+2)
- [x] Bereit für Test-Ausführung (erwarte Fehler: KrokiClient nicht importiert)

## Green

### Phase Entrance Criteria:
- [x] 2 Tests geschrieben und schlagen fehl (RED)
- [x] Tests schlagen aus dem richtigen Grund fehl (KrokiClient nicht importiert)
- [x] Tests validieren erwartete Funktionalität (Validation + Retry)
- [x] Test-Typ: Unit-Tests mit Mocks (wie Cycle 1+2)

### Tasks
- [x] **Orchestrator (Zyklus 3):** KrokiClient-Integration implementieren
- [x] KrokiClient + KrokiRenderError import hinzufügen
- [x] KrokiClient im __init__ instantiieren (mit settings.kroki_local_url)
- [x] render_diagram() im Iteration-Loop aufrufen
- [x] try/except für KrokiRenderError implementieren
- [x] Refinement-Prompt bei Error bauen (enthält error + previous source)
- [x] Bei Success: break aus Loop
- [x] Alte Tests anpassen: KrokiClient mocken + kroki_local_url hinzufügen
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] KrokiClient + KrokiRenderError importiert ✅
- [x] self.kroki_client = KrokiClient(settings.kroki_local_url) in __init__ ✅
- [x] Validation-Loop implementiert: try { render_diagram() } catch { refinement } ✅
- [x] Refinement-Prompt: "Fix the following {type} diagram. Previous attempt had this error: {error}" ✅
- [x] Alte Tests gefixt: KrokiClient-Mock + kroki_local_url hinzugefügt ✅
- [x] 5 Tests passed! ✅ (92% Coverage für Orchestrator)

## Refactor

### Phase Entrance Criteria:
- [x] Der Test ist grün (PASS)
- [x] Implementation ist vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [x] Die Lösung adressiert das eigentliche Problem

### Tasks
- [x] **Orchestrator (Zyklus 3):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft: KrokiClient + KrokiRenderError imports korrekt ✓
- [x] Error-Handling validiert: try/except sauber, validation_error tracking ✓
- [x] Refinement-Prompt Format: Klar und vollständig (error + description + previous source) ✓
- [x] Potentielle Refactorings geprüft: Prompt extraction → YAGNI (nur 4 Zeilen) ✓
- [x] Pattern-Konsistenz: Analog zu LLMClient-Integration ✓
- [x] Keine Refactorings nötig - Code ist clean

### Completed
- [x] Code Review durchgeführt: Keine Änderungen nötig ✅
- [x] Pattern konsistent (Dependency Injection, Error-Handling mit try/except)
- [x] Docstrings vollständig, Type hints angemessen
- [x] Tests passed ✅ (92% Coverage für Orchestrator)
- [x] Orchestrator Zyklus 3 abgeschlossen ✅ (KrokiClient Validation-Loop)

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
**Status**: 3 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Zyklus 1: Iteration-Loop mit max_iterations + max_time_seconds
- ✅ Zyklus 2: LLMClient-Integration für echte Generierung
- ✅ Zyklus 3: KrokiClient Validation-Loop mit Error-Retry
- ✅ 5 Tests, 92% Coverage
- ✅ stopped_reason Logic (max_iterations | max_time | success)

**Implementiert:**
- Iteration-Loop mit while iterations_used < max_iterations
- Zeit-Tracking mit time.time() (start + elapsed)
- Limits aus Settings (max_iterations=5, max_time_seconds=60)
- Metadata: iterations_used, elapsed_seconds, stopped_reason
- LLMClient-Integration: self.llm_client = LLMClient(settings)
- KrokiClient-Integration: self.kroki_client = KrokiClient(settings.kroki_local_url)
- Validation-Loop: try { render_diagram() } catch { refinement prompt }
- Refinement-Prompt: "Fix the following {type} diagram. Previous attempt had this error: {error}..."
- Autonome Iteration bis Syntax valid oder Limits erreicht

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
