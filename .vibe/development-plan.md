# Development Plan: diag-agent (main branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
MCP Server Implementation: FastMCP-basierter Server für diag-agent, der die Diagramm-Generierung als MCP-Tool für andere LLM-Anwendungen verfügbar macht

## Explore
### Tasks
*All exploration completed*

### Completed
- [x] Created development plan file
- [x] FastMCP researched und verstanden (Python-Framework für MCP-Server)
- [x] pyproject.toml analysiert - FastMCP bereits als optionale Dependency vorhanden
- [x] Orchestrator.execute() analysiert - Hauptfunktionalität identifiziert
- [x] Settings-Architektur verstanden (ENV-basierte Konfiguration)
- [x] MCP-Anforderungen definiert: Ein Tool "create_diagram" exponieren
- [x] Test-Strategie definiert: Unit Tests für MCP Tool mit Orchestrator-Mock

## Red

### Phase Entrance Criteria:
- [x] MCP-Protokoll und FastMCP Library sind verstanden
- [x] Scope und Requirements für den MCP Server sind klar definiert
- [x] Bestehende diag-agent Architektur ist analysiert
- [x] Integration-Points zwischen MCP Server und Orchestrator sind identifiziert
- [x] Test-Strategie ist definiert

### Tasks
*All tests written and validated*

### Completed
- [x] Test 1: `test_mcp_server_initialization` geschrieben
- [x] Test 2: `test_create_diagram_tool_success` geschrieben
- [x] Test 3: `test_create_diagram_with_custom_parameters` geschrieben
- [x] Test 4: `test_create_diagram_returns_correct_structure` geschrieben
- [x] Test 5: `test_create_diagram_error_handling` geschrieben
- [x] Alle Tests ausgeführt - alle 5 Tests schlagen erwartungsgemäß fehl (ImportError: mcp/create_diagram nicht gefunden)

## Green

### Phase Entrance Criteria:
- [x] Tests sind geschrieben und schlagen erwartungsgemäß fehl
- [x] Test-Failures zeigen die fehlende Funktionalität klar auf
- [x] Alle Tests wurden ausgeführt und validiert

### Tasks
*All implementation completed*

### Completed
- [x] FastMCP installiert (`pip install fastmcp`)
- [x] MCP Server implementiert in `src/diag_agent/mcp/server.py`
- [x] FastMCP Server initialisiert mit Namen "diag-agent"
- [x] `create_diagram` Funktion implementiert (wrappet Orchestrator.execute())
- [x] create_diagram Tool bei MCP Server registriert via `mcp.tool()`
- [x] Test für list_tools() Fix (verwendet private API korrekt)
- [x] Alle 5 MCP Tests sind grün ✅
- [x] Alle 56 Unit Tests sind grün ✅
- [x] Coverage: 86% (MCP Server: 92%)

## Refactor

### Phase Entrance Criteria:
- [x] Implementierung ist abgeschlossen
- [x] Alle Tests sind grün
- [x] Funktionalität ist vollständig und korrekt

### Tasks
*No refactoring needed*

### Completed
- [x] Code Review durchgeführt
- [x] Keine Code-Duplikation gefunden (nur eine Funktion)
- [x] Namen sind klar und selbsterklärend
- [x] YAGNI-Prinzip wird eingehalten
- [x] Dependency Injection geprüft → nicht sinnvoll für simplen Wrapper
- [x] Error Handling geprüft → FastMCP handled automatisch
- [x] Keine offensichtlichen Verbesserungen notwendig

## Key Decisions

### EXPLORE Phase
1. **FastMCP als Framework**: Version 2.0 gewählt - production-ready, Pythonic, gut dokumentiert
2. **Ein Tool "create_diagram"**: Exponiert Orchestrator.execute() direkt als MCP Tool
3. **Keine zusätzlichen Resources/Prompts**: YAGNI - nur das Tool wird gebraucht
4. **Test-Strategie**: Unit Tests mit Orchestrator-Mocking für schnelle, isolierte Tests

### GREEN Phase
1. **Funktion vor Decorator**: `create_diagram` als normale Funktion definiert, dann mit `mcp.tool()` registriert - ermöglicht direktes Testen
2. **Settings in Tool laden**: Jeder Request lädt frische Settings (kein Caching) - verhindert stale configuration
3. **Direkte Orchestrator-Integration**: Kein zusätzlicher Layer zwischen Tool und Orchestrator - KISS-Prinzip
4. **Error Propagation**: Exceptions werden nicht gefangen - FastMCP handled automatisch

### REFACTOR Phase
1. **Code Review**: Keine Refactorings nötig - Code ist bereits optimal
2. **Begründung Dependency Injection**: Für simplen Wrapper unnötig - würde Tests komplizierter machen ohne Mehrwert
3. **Begründung kein Error Handling**: FastMCP handled Exceptions automatisch und gibt sie korrekt an Client weiter

## Notes

### FastMCP Framework (Researched)
**Was ist FastMCP?**
- Python-Framework für Model Context Protocol (MCP) Server
- "The fast, Pythonic way to build MCP servers"
- Version 2.0 ist production-ready mit Enterprise-Features

**Installation**: `pip install fastmcp` (bereits in pyproject.toml als optional-dependency)

**Basic Pattern**:
```python
from fastmcp import FastMCP

mcp = FastMCP("Server Name")

@mcp.tool
def my_tool(param: str) -> str:
    """Tool description"""
    return "result"
```

**MCP Capabilities**:
1. **Tools** - Ausführbare Funktionen (wie POST endpoints)
2. **Resources** - Daten-Quellen für Kontext (wie GET endpoints)
3. **Prompts** - Wiederverwendbare LLM-Templates

### Orchestrator Integration (Analyzed)
**Hauptfunktion**: `Orchestrator.execute()`
- **Input**: description (str), diagram_type (str), output_dir (str), output_formats (str)
- **Output**: Dict mit diagram_source, output_path, iterations_used, elapsed_seconds, stopped_reason
- **Logic**: Iterative LLM-Generation + Kroki-Validierung + optionale Design-Analyse

### Requirements Definition
**MCP Tool**: `create_diagram`
- Exponiert Orchestrator.execute() als MCP-Tool
- Parameter: description, diagram_type, output_dir, output_formats
- Return: JSON mit Diagramm-Quelle und Metadaten

**Implementierung**:
- Server-Datei: `src/diag_agent/mcp/server.py`
- Tool-Funktion mit @mcp.tool Decorator
- Settings-Integration für Konfiguration
- Orchestrator-Instanz erstellen und execute() aufrufen

### Test-Strategie
**Unit Tests** (tests/unit/test_mcp_server.py):
1. Test MCP Server Initialisierung
2. Test create_diagram Tool mit gemocktem Orchestrator
3. Test Parameter-Validierung
4. Test Error-Handling (z.B. ungültiger diagram_type)
5. Test Settings-Integration

**Mocking**:
- Mock Orchestrator.execute() für predictable Outputs
- Mock Settings für Test-Konfiguration

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
