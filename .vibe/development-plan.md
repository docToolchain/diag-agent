# Development Plan: diag-agent (main branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
CLI Examples Command: Implementierung eines `diag-agent examples` Commands zum Abrufen und Anzeigen von Beispiel-Diagrammen für verschiedene Diagramm-Typen (initial: C4-PlantUML, BPMN).

## Explore
### Tasks
*All exploration tasks completed*

### Completed
- [x] Created development plan file
- [x] TDD-Workflow gestartet
- [x] Entrance Criteria für alle Phasen definiert
- [x] Anforderungen analysiert und dokumentiert (User Story, funktionale/nicht-funktionale Requirements)
- [x] CLI-Struktur analysiert (Click-Framework, commands.py Pattern)
- [x] Beispiel-Diagramme erstellt (3x C4-PlantUML, 2x BPMN)
- [x] Ordnerstruktur implementiert (src/diag_agent/examples/{c4plantuml,bpmn}/)
- [x] Test-Strategie definiert (5 Unit Tests, keine Mocks für File-System)

## Red

### Phase Entrance Criteria:
- [x] Anforderungen und Scope sind klar definiert
- [x] Codebase-Struktur ist verstanden (CLI, Beispiele-Ordner)
- [x] Beispiel-Diagramme sind verfügbar (C4-PlantUML, BPMN)
- [x] Test-Strategie ist definiert

### Tasks
*All tests written and validated*

### Completed
- [x] Test 1: `test_examples_list_shows_all_examples` geschrieben
- [x] Test 2: `test_examples_list_filters_by_type` geschrieben
- [x] Test 3: `test_examples_show_displays_source_code` geschrieben
- [x] Test 4: `test_examples_show_handles_nonexistent` geschrieben
- [x] Test 5: `test_examples_list_output_context_efficient` geschrieben
- [x] Alle Tests ausgeführt - alle 5 Tests schlagen erwartungsgemäß fehl (No such command 'examples')

## Green

### Phase Entrance Criteria:
- [x] Tests sind geschrieben und schlagen erwartungsgemäß fehl
- [x] Test-Failures zeigen die fehlende Funktionalität klar auf
- [x] Alle Tests wurden ausgeführt und validiert

### Tasks
*All implementation completed*

### Completed
- [x] Click Group "examples" in commands.py erstellt
- [x] Subcommand "list" mit --type Filter implementiert
- [x] Subcommand "show" mit example_name Argument implementiert
- [x] Helper-Funktion `_get_examples_dir()` zum Lokalisieren des examples/ Ordners
- [x] Helper-Funktion `_list_examples()` zum Auflisten aller Beispiele mit Filter
- [x] Helper-Funktion `_load_example()` zum Laden eines Beispiels
- [x] Fehlerbehandlung für nicht-existierende Beispiele (FileNotFoundError, ValueError)
- [x] Alle 5 neuen Tests sind grün ✅
- [x] Alle 44 Unit Tests sind grün ✅
- [x] Coverage: 90% (CLI: 57% → 83%)

## Refactor

### Phase Entrance Criteria:
- [x] Implementierung ist abgeschlossen
- [x] Alle Tests sind grün
- [x] Funktionalität ist vollständig und korrekt

### Tasks
*No refactoring needed*

### Completed
- [x] Code Review durchgeführt
- [x] Keine Code-Duplikation gefunden
- [x] Namen sind klar und selbsterklärend
- [x] YAGNI-Prinzip wird eingehalten
- [x] Error Handling ist robust und explizit
- [x] Keine offensichtlichen Verbesserungen notwendig

## Key Decisions

### EXPLORE Phase
1. **Beispiel-Quellen**: Standard-Beispiele aus C4-PlantUML Repository und BPMN-Spec verwendet (Kroki-Doku-Zugriff fehlgeschlagen)
2. **Ordnerstruktur**: `src/diag_agent/examples/{type}/` - erweiterbar durch einfaches Hinzufügen neuer Files
3. **CLI-Pattern**: Click Group `examples` mit Subcommands `list` und `show` (analog zu git-Pattern)
4. **Test-Strategie**: Keine Mocks für File-System - Tests validieren echte Beispiel-Files (Teil des Package)
5. **Initial Scope**: C4-PlantUML (3 Beispiele) + BPMN (2 Beispiele) - weitere Typen später erweiterbar

### GREEN Phase
1. **Implementation**: 3 Helper-Funktionen + 2 Click Commands (list, show)
2. **Path Resolution**: `Path(__file__).parent.parent / "examples"` für robuste Pfad-Auflösung
3. **File Extension Mapping**: Dictionary für Typ → Extensions (c4plantuml: .puml, bpmn: .bpmn, etc.)
4. **Error Handling**: FileNotFoundError für missing examples, ValueError für invalid format
5. **Output Format**: Gruppiert nach Typ, context-efficient (<2000 chars)

### REFACTOR Phase
1. **Code Review**: Keine Duplikation, klare Namen, YAGNI-konform
2. **Keine Refactorings nötig**: Code ist bereits gut strukturiert
3. **Begründung**: Extensions inline (YAGNI), Error-Handling explizit (verschiedene Messages), Output-Logik klar

## Notes

### Anforderungen (Requirements)
**User Story**: Als Entwickler möchte ich Beispiel-Diagramme abrufen können, um die Syntax verschiedener Diagramm-Typen zu lernen und als Vorlage zu nutzen.

**Funktionale Anforderungen**:
- `diag-agent examples list` - Zeigt alle verfügbaren Beispiele an
- `diag-agent examples list --type c4plantuml` - Filtert nach Diagramm-Typ
- `diag-agent examples show <name>` - Zeigt ein spezifisches Beispiel an (Source-Code)
- Initial Support für: C4-PlantUML, BPMN

**Nicht-Funktionale Anforderungen**:
- Beispiele als Files im Package (werden mit pip installiert)
- Einfach erweiterbar (neues File = neues Beispiel)
- Context-effiziente CLI-Ausgabe (<500 tokens für LLM)

### Beispiel-Diagramme (aus C4-PlantUML & BPMN Standards)

**C4-PlantUML Beispiele**:
1. **context-diagram.puml** - System Context Diagram
2. **container-diagram.puml** - Container Diagram
3. **component-diagram.puml** - Component Diagram

**BPMN Beispiele**:
1. **simple-process.bpmn** - Einfacher Prozess
2. **collaboration.bpmn** - Kollaboration mit Pools

### Ordnerstruktur
```
src/diag_agent/examples/
├── c4plantuml/
│   ├── context-diagram.puml
│   ├── container-diagram.puml
│   └── component-diagram.puml
└── bpmn/
    ├── simple-process.bpmn
    └── collaboration.bpmn
```

### CLI-Struktur (Analyse von commands.py)
- Framework: Click (ADR-008)
- Existing: `@cli.command()` für `create`
- Neu: `@cli.group()` für `examples` mit Subcommands `list` und `show`
- Pattern: CliRunner für Tests (siehe test_cli.py)

### Test-Strategie

**Unit Tests** (tests/unit/test_cli.py):
1. `test_examples_list_shows_all_examples` - List ohne Filter zeigt alle Beispiele
2. `test_examples_list_filters_by_type` - List mit --type Filter
3. `test_examples_show_displays_source_code` - Show zeigt Beispiel-Source
4. `test_examples_show_handles_nonexistent` - Show mit ungültigem Namen
5. `test_examples_list_output_context_efficient` - Ausgabe < 500 tokens

**Test-Daten**:
- Mock examples Files oder echte Minimal-Beispiele in fixtures
- Verwende pathlib.Path für Plattform-Kompatibilität

**Mocking-Strategie**:
- Mocke File-System-Zugriffe NICHT (echte Beispiel-Files verwenden)
- Reason: Beispiele sind Teil des Package, Tests validieren echte Daten

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
