# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore
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
- [x] Test für Kroki Client schreiben: `test_render_diagram_success()` (Happy-Path)
- [x] Test ausführen und Fehlschlag verifizieren (RED)
- [x] Test-Entscheidungen dokumentieren

### Completed
- [x] Unit-Test geschrieben (mit HTTP-Mock, httpx)
- [x] Test validiert: Diagram-Source → Kroki HTTP POST → PNG-Response
- [x] Test schlägt fehl: `ImportError: KrokiClient` nicht gefunden (erwartet)

## Green

### Phase Entrance Criteria:
- [ ] Ein spezifischer, fokussierter Test wurde geschrieben
- [ ] Der Test schlägt fehl (RED) aus dem richtigen Grund
- [ ] Test validiert tatsächlich die erwartete Funktionalität
- [ ] Test-Typ (Unit/Integration) wurde mit User abgestimmt

### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Refactor

### Phase Entrance Criteria:
- [ ] Der Test ist grün (PASS)
- [ ] Implementation ist vollständig und funktionsfähig
- [ ] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [ ] Die Lösung adressiert das eigentliche Problem

### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Key Decisions

### Architektur-Entscheidungen (aus ADRs)
- **ADR-001**: Bash-Tool mit `--help` ist primär, MCP optional → Context-Effizienz
- **ADR-002**: Agent iteriert selbständig mit eigenem LLM-Client → Autonomie
- **ADR-003**: Local-First (Kroki Fat-JAR), kroki.io nur mit Consent → Privacy
- **ADR-005**: LiteLLM für Provider-Abstraction → 100+ Modelle unterstützt
- **ADR-006**: Docker mit gebundeltem Kroki (Fat-JAR) → Einfache Installation
- **ADR-008**: Click als CLI Framework → Rich UX, LLM-kompatibel

### Tech Stack
- **Python**: 3.10+ (bestehende Expertise)
- **CLI**: Click (intuitive commands, gute Help-Ausgabe)
- **LLM**: LiteLLM (Provider-agnostisch)
- **MCP**: FastMCP (Standard-Protokoll)
- **Rendering**: Kroki (20+ Diagramm-Typen)
- **Config**: python-dotenv, PyYAML
- **HTTP**: requests/httpx

### Qualitätsziele (Priorität)
1. **Context Efficiency**: < 3k tokens pro Diagramm-Request
2. **Ease of Installation**: < 5 Min bis zum ersten Diagramm
3. **Privacy & Security**: Local-First, kein Remote ohne Consent
4. **Autonomy**: Agent iteriert ohne Parent-LLM Intervention
5. **Extensibility**: Alle Kroki-Typen, einfacher Provider-Wechsel

### Test-Strategie (RED-Phase)
- **Test-Typ**: Unit-Test mit HTTP-Mock (pytest + unittest.mock)
- **Fokus**: Happy-Path zuerst, Error-Cases in separaten Tests
- **Design**: Generisches Interface für alle Kroki-Diagram-Typen
- **Erster Test**: `test_render_diagram_success()` - PlantUML → PNG

## Notes

### MVP-Strategie: Bottom-Up mit Kroki Client
**Erste Komponente: Kroki Client** (`src/diag_agent/kroki/client.py`)
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
