# Development Plan: diag-agent (main branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
CLI Kroki Management Commands: Implementierung von `diag-agent kroki` Commands für Docker-basiertes Kroki-Management (start, stop, status, logs)

## Explore
### Tasks
*All exploration tasks completed*

### Completed
- [x] Created development plan file
- [x] TDD-Workflow gestartet
- [x] Entrance Criteria für alle Phasen definiert
- [x] Anforderungen analysiert und dokumentiert (4 Commands: start/stop/status/logs)
- [x] KrokiManager API analysiert (start, stop, is_running, health_check)
- [x] CLI-Pattern analysiert (@cli.group() → @kroki.command())
- [x] Test-Strategie definiert (7 Unit Tests mit KrokiManager Mocks)
- [x] Docker logs Zugriff: `docker logs kroki [--follow]` via subprocess

## Red

### Phase Entrance Criteria:
- [x] Anforderungen und Scope sind klar definiert
- [x] KrokiManager API ist verstanden
- [x] CLI-Pattern ist analysiert
- [x] Test-Strategie ist definiert

### Tasks
*All tests written and validated*

### Completed
- [x] Test 1: `test_kroki_start_command_starts_container` geschrieben
- [x] Test 2: `test_kroki_stop_command_stops_container` geschrieben
- [x] Test 3: `test_kroki_status_shows_running_and_healthy` geschrieben
- [x] Test 4: `test_kroki_status_shows_stopped` geschrieben
- [x] Test 5: `test_kroki_logs_displays_container_logs` geschrieben
- [x] Test 6: `test_kroki_start_handles_docker_not_installed` geschrieben
- [x] Test 7: `test_kroki_logs_follow_mode` geschrieben
- [x] Alle Tests ausgeführt - alle 7 Tests schlagen erwartungsgemäß fehl (KrokiManager/subprocess not found)

## Green

### Phase Entrance Criteria:
- [x] Tests sind geschrieben und schlagen erwartungsgemäß fehl
- [x] Test-Failures zeigen die fehlende Funktionalität klar auf
- [x] Alle Tests wurden ausgeführt und validiert

### Tasks
*All implementation completed*

### Completed
- [x] Import KrokiManager und subprocess in commands.py
- [x] Click Group "kroki" erstellt
- [x] Command "start" implementiert (mit KrokiManagerError Handling)
- [x] Command "stop" implementiert
- [x] Command "status" implementiert (running/stopped, healthy/unhealthy)
- [x] Command "logs" implementiert (mit --follow Option)
- [x] Alle 7 neuen Tests sind grün ✅
- [x] Alle 51 Unit Tests sind grün ✅
- [x] Coverage: 86% (CLI: 77%)

## Refactor

### Phase Entrance Criteria:
- [x] Implementierung ist abgeschlossen
- [x] Alle Tests sind grün
- [x] Funktionalität ist vollständig und korrekt

### Tasks
*No refactoring needed*

### Completed
- [x] Code Review durchgeführt
- [x] Keine Code-Duplikation gefunden (Error-Handling Patterns sind zu kurz für Extraktion)
- [x] Namen sind klar und selbsterklärend
- [x] YAGNI-Prinzip wird eingehalten
- [x] Error Handling ist robust und konsistent
- [x] Keine offensichtlichen Verbesserungen notwendig

## Key Decisions

### EXPLORE Phase
1. **4 Commands definiert**: start, stop, status, logs (analog zu docker CLI)
2. **Click Group Pattern**: `@cli.group()` → `@kroki.command()` (konsistent mit examples)
3. **subprocess für logs**: Direkter Zugriff via `docker logs` (kein Wrapper in KrokiManager nötig)
4. **Test-Strategie**: KrokiManager mocken, subprocess mocken für logs

### GREEN Phase
1. **Error Handling**: KrokiManagerError separat catchen für spezifische Messages
2. **Status Logic**: is_running() → health_check() nur wenn running (Optimierung)
3. **Logs Implementation**: subprocess.run mit check=True, capture_output für Output
4. **Success Messages**: Benutzerfreundliche Messages mit Checkmarks (✓)

### REFACTOR Phase
1. **Code Review**: Keine Duplikation, klare Namen, YAGNI-konform
2. **Keine Refactorings nötig**: Error-Handling Patterns zu kurz für Abstraktion
3. **Begründung**: Commands sind unabhängig, inline Error-Handling ist klarer als Abstraktion

## Notes

### Anforderungen (Requirements)
**User Story**: Als Entwickler möchte ich Kroki Docker-Container über die CLI verwalten können, um einfach zwischen lokalem und Remote-Modus zu wechseln.

**Funktionale Anforderungen**:
- `diag-agent kroki start` - Startet Kroki Docker Container
- `diag-agent kroki stop` - Stoppt und entfernt Kroki Container
- `diag-agent kroki status` - Zeigt Status an (running/stopped, healthy/unhealthy)
- `diag-agent kroki logs [--follow]` - Zeigt Container-Logs an

**Nicht-Funktionale Anforderungen**:
- Benutzerfreundliche Fehlermeldungen (z.B. "Docker not installed")
- Status-Output klar und informativ
- Logs unterstützen Follow-Modus für Live-Anzeige

### KrokiManager API (Analysiert)
**Methoden**:
- `start()` - Startet Container (raises KrokiManagerError)
- `stop()` - Stoppt und entfernt Container (raises KrokiManagerError)
- `is_running() -> bool` - Prüft ob Container läuft
- `health_check() -> bool` - Prüft ob HTTP-Service antwortet

**Konstanten**:
- `CONTAINER_NAME = "kroki"`
- `DEFAULT_PORT = 8000`
- `DOCKER_IMAGE = "yuzutech/kroki"`

### CLI-Pattern (Analysiert)
**Click Structure** (siehe commands.py):
- `@cli.group()` - Definiert Command-Gruppe (z.B. `examples`)
- `@group_name.command()` - Definiert Subcommand (z.B. `examples list`)
- Pattern für `kroki`: `@cli.group()` → `@kroki.command(name="start")`

**Analog zu `examples` Group**:
```python
@cli.group()
def kroki():
    """Manage local Kroki Docker container."""
    pass

@kroki.command(name="start")
def start_kroki():
    """Start Kroki container."""
```

### Test-Strategie

**Unit Tests** (tests/unit/test_cli.py):
1. `test_kroki_start_command_starts_container` - Startet Container erfolgreich
2. `test_kroki_stop_command_stops_container` - Stoppt Container erfolgreich
3. `test_kroki_status_shows_running_and_healthy` - Status zeigt "running + healthy"
4. `test_kroki_status_shows_stopped` - Status zeigt "stopped"
5. `test_kroki_logs_displays_container_logs` - Logs zeigen Container-Output
6. `test_kroki_start_handles_docker_not_installed` - Fehlerbehandlung für fehlendes Docker
7. `test_kroki_logs_follow_mode` - Logs mit --follow Option

**Mocking-Strategie**:
- Mock `KrokiManager` Instanz und Methoden
- Mock `subprocess.run` für `docker logs` Command
- Verwende Click's `CliRunner` für Command-Testing

**Test-Daten**:
- Mock Container-Status (running/stopped)
- Mock Health-Check Responses (True/False)
- Mock Logs-Output (String mit typischen Log-Lines)

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
