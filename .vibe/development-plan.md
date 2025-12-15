# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore

### Phase Entrance Criteria:
- [ ] Es ist klar, welche Komponente als nächstes implementiert werden soll
- [ ] Architektur-Dokumentation zu Config Management gelesen
- [ ] Bestehende Patterns und Konventionen verstanden
- [ ] Config-Precedence-Rules dokumentiert

### Tasks
- [x] Arc42-Dokumentation durchgehen und Key Requirements extrahieren
- [x] Alle 8 ADRs lesen und Architektur-Entscheidungen verstehen
- [x] Tech Stack und Dependencies definieren (Python 3.10+, LiteLLM, Click, FastMCP, etc.)
- [x] Projekt-Struktur anlegen (src-Layout mit Tests)
- [x] Qualitätsziele und Constraints aus arc42 zusammenfassen
- [x] Erste Komponente für MVP identifizieren: **Kroki Client**

### Completed
- [x] Created development plan file
- [x] Entrance criteria für alle Phasen definiert
- [x] Alle 8 ADRs lesen und Architektur-Entscheidungen verstehen
- [x] Arc42-Dokumentation durchgehen und Key Requirements extrahieren
- [x] Tech Stack und Dependencies definieren (Python 3.10+, LiteLLM, Click, FastMCP, etc.)
- [x] Qualitätsziele und Constraints aus arc42 zusammenfassen
- [x] Projekt-Struktur erstellt (src-Layout mit allen Modulen)
- [x] pyproject.toml, .env.example, README erstellt
- [x] MVP-Komponente identifiziert: **Kroki Client**

## Red

### Phase Entrance Criteria:
- [x] Exploration ist abgeschlossen und Anforderungen sind dokumentiert
- [x] Architektur-Entscheidungen aus arc42-Dokumentation sind verstanden
- [x] Bestehende Patterns und Konventionen sind erfasst
- [x] Es ist klar, welche Funktionalität als nächstes implementiert werden soll

### Tasks
- [x] **Config Management:** Tests für Settings-Klasse schreiben
- [x] Test 1: `test_load_settings_with_defaults` - Defaults ohne ENV
- [x] Test 2: `test_load_settings_from_env` - ENV vars überschreiben
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 2 Unit-Tests in tests/unit/test_settings.py geschrieben
- [x] Test 1 validiert: 7 Default-Werte (llm_provider, kroki_mode, max_iterations, etc.)
- [x] Test 2 validiert: ENV override + Type conversion (str→int)
- [x] Tests schlagen fehl: `ImportError: Settings` (erwartet) ✅

## Green

### Phase Entrance Criteria:
- [x] Ein spezifischer, fokussierter Test wurde geschrieben
- [x] Der Test schlägt fehl (RED) aus dem richtigen Grund
- [x] Test validiert tatsächlich die erwartete Funktionalität
- [x] Test-Typ (Unit/Integration) wurde mit User abgestimmt

### Tasks
- [x] **Config Management:** Settings-Klasse implementieren
- [x] dataclass mit __init__ für ENV var loading
- [x] python-dotenv Integration (load_dotenv())
- [x] Type conversion für Integer-Werte (max_iterations, max_time_seconds)
- [x] Tests ausführen und grün machen

### Completed
- [x] Settings-Klasse in src/diag_agent/config/settings.py erstellt
- [x] 7 Config-Optionen implementiert mit Defaults aus .env.example
- [x] ENV var loading mit DIAG_AGENT_ prefix
- [x] Type-safe Integer Conversion (str→int)
- [x] Beide Tests passed! ✅ (100% Coverage)
- [x] **Zyklus 2:** KrokiRenderError Exception mit klarer Docstring
- [x] **Zyklus 2:** try-except Block für httpx.HTTPStatusError
- [x] **Zyklus 2:** Error-Message mit status code + diagram type
- [x] Beide Tests passed! ✅ (100% Coverage)

## Refactor

### Phase Entrance Criteria:
- [x] Der Test ist grün (PASS)
- [x] Implementation ist vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [x] Die Lösung adressiert das eigentliche Problem

### Tasks
- [x] **Config Management:** Code Review durchführen
- [x] Robustness-Issue identifiziert: int() ohne Error-Handling
- [x] Test für ungültige Integer-Werte schreiben
- [x] Helper-Methode _get_int_env() extrahieren
- [x] Tests validieren (alle grün ✓)

### Completed
- [x] Test `test_invalid_integer_value_uses_default` hinzugefügt
- [x] Helper-Methode `_get_int_env()` für sichere Type Conversion
- [x] Graceful fallback zu defaults bei ValueError
- [x] Config Management TDD-Zyklus abgeschlossen ✅ (100% Coverage, 3 Tests)

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
