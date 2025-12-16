# Development Plan: diag-agent (main branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Transparente CLI-Ausgabe mit Progress-Updates und LLM-Feedback-Logging während der Diagramm-Generierung

**Problem**: 
Der Generierungsprozess ist intransparent - Nutzer sehen nur das Endergebnis, nicht was währenddessen passiert.

**Ziel**:
1. **Progress-Updates**: Während der Generierung soll sichtbar sein, was gerade passiert (Iteration X/Y, Validierung, Design-Feedback, etc.)
2. **LLM-Feedback-Log**: Log-Ausgabe, in der das LLM erklärt, was nicht gut war und was es verbessern möchte (validation_error, design_feedback)

## Explore

### Tasks
*All exploration completed*

### Completed
- [x] Created development plan file
- [x] Code-Analyse: CLI create() Funktion (src/diag_agent/cli/commands.py)
- [x] Code-Analyse: Orchestrator.execute() Methode (src/diag_agent/agent/orchestrator.py)
- [x] User-Feedback erhalten: Wenig Konsole (LLM-Kontext!), ausführliches Log im output-dir
- [x] Anforderungen definiert (siehe Key Decisions)
- [x] Bestehende Logging-Infrastruktur analysieren (keine vorhanden)
- [x] Design-Entscheidung dokumentiert (Zwei-Ebenen-Strategie)

### Completed
- [x] Created development plan file

## Red

### Phase Entrance Criteria:
- [x] Progress-Update-Anforderungen sind klar definiert (welche Meldungen, wann?)
- [x] LLM-Feedback-Format ist definiert
- [x] Design-Entscheidung für Output-Mechanismus ist getroffen (Callback/Logger/Print)
- [x] Bestehende Code-Struktur ist verstanden
- [x] Test-Strategie ist klar

### Tasks
*All tests written and validated*

### Completed
- [x] Test 1: Orchestrator erstellt generation.log in output_dir
- [x] Test 2: Orchestrator loggt Iteration-Start (Iteration X/Y - START)
- [x] Test 3: Orchestrator loggt LLM-Prompts (initial)
- [x] Test 4: Orchestrator loggt Validation Errors
- [x] Test 5: Orchestrator loggt Design Feedback
- [x] Test 6: Orchestrator loggt Refinement Prompts
- [x] Test 7: CLI zeigt minimale Progress-Updates auf Konsole
- [x] Alle Tests ausgeführt - alle 7 Tests schlagen erwartungsgemäß fehl
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Green

### Phase Entrance Criteria:
- [x] Tests sind geschrieben und schlagen erwartungsgemäß fehl
- [x] Test-Failures zeigen die fehlende Funktionalität klar auf
- [x] Alle Tests wurden ausgeführt und validiert

### Tasks
*All implementation completed*

### Completed
- [x] Orchestrator: Logger-Setup mit FileHandler für generation.log
- [x] Orchestrator: Log Iteration Start (Iteration X/Y - START)
- [x] Orchestrator: Log LLM Prompt (initial, syntax fix, design refinement)
- [x] Orchestrator: Log Validation Success/Error
- [x] Orchestrator: Log Design Feedback
- [x] Orchestrator: progress_callback Parameter für CLI-Progress
- [x] CLI: Progress-Callback implementiert mit click.echo()
- [x] CLI: Zeigt "See generation.log for details" am Ende
- [x] Alle Tests ausgeführt - alle 68 Tests grün ✅
- [x] Coverage: 87% (Orchestrator: 98%)

### Completed
*None yet*

## Refactor

### Phase Entrance Criteria:
- [x] Implementierung ist abgeschlossen
- [x] Alle Tests sind grün
- [x] Funktionalität ist vollständig und korrekt

### Tasks
*No refactoring needed*

### Completed
- [x] Code Review durchgeführt
- [x] Logger-Setup in _setup_file_logger() extrahiert
- [x] Logger-Cleanup in _cleanup_logger() extrahiert
- [x] Naming ist klar und selbsterklärend
- [x] Keine Duplikation gefunden
- [x] Alle Tests nach Refactoring grün (68/68) ✅
- [x] Coverage: 87% (Orchestrator: 98%)

### Completed
*None yet*

## Summary

**Feature Complete! ✅**

Transparente CLI-Ausgabe mit Progress-Updates und LLM-Feedback-Logging wurde erfolgreich implementiert.

**Ergebnis**:
- ✅ 68/68 Tests grün
- ✅ Coverage: 87% (Orchestrator: 98%)
- ✅ Minimale Konsolen-Ausgabe (schont LLM-Kontext)
- ✅ Ausführliches Log in generation.log

**Konsolen-Ausgabe** (minimal):
```
Generating diagram... [Iteration 1/10]
✓ Diagram generated: diagrams/diagram.png
  Source: 324 characters
  Iterations: 2
  Time: 4.5s
  Stopped: success
  See generation.log for details
```

**Log-Datei** (ausführlich): `{output_dir}/generation.log`
- Timestamps für jede Iteration
- Komplette LLM-Prompts (initial, syntax fix, design refinement)
- Validation errors mit Details
- Design feedback komplett
- Iteration outcomes

## Key Decisions

### EXPLORE Phase

**1. Zwei-Ebenen-Ausgabe-Strategie**

**Problem**: Konsolen-Ausgabe landet im Kontext des aufrufenden LLMs → muss minimal sein!

**Lösung**:
- **Konsole (stdout)**: Kompakt, nur Progress-Indicator
  - "Iteration 1/10..." (während Iteration läuft)
  - "✓ Diagram generated" (am Ende wie bisher)
  - Keine detaillierten Fehler/Feedback auf Konsole!
  
- **Log-Datei** (`{output_dir}/generation.log`): Ausführlich
  - Alle Iterationen mit Timestamps
  - Komplette LLM-Prompts (initial, refinement)
  - Validation errors (kompletter Kroki-Fehler)
  - Design feedback (komplettes LLM-Feedback)
  - Iteration outcomes (success/error/improvement)

**2. Anforderungen**

**Konsolen-Ausgabe** (minimalistisch):
```
Generating diagram... [Iteration 1/10]
Generating diagram... [Iteration 2/10]
✓ Diagram generated: diagrams/diagram.png
  See generation.log for details
```

**Log-Datei** (ausführlich):
```
2025-12-16 20:54:36 - Iteration 1/10 - START
2025-12-16 20:54:36 - LLM Prompt (initial):
  Generate a plantuml diagram: User authentication flow
2025-12-16 20:54:38 - LLM Response: 216 characters
2025-12-16 20:54:38 - Kroki Validation: SUCCESS
2025-12-16 20:54:38 - Iteration 1/10 - COMPLETE (syntax valid)

2025-12-16 20:54:38 - Iteration 2/10 - START
2025-12-16 20:54:38 - Design Analysis: ANALYZING
2025-12-16 20:54:40 - Design Feedback:
  Layout is too cramped. Increase vertical spacing between
  components. Add more descriptive labels.
2025-12-16 20:54:40 - LLM Prompt (design refinement):
  Improve the following plantuml diagram based on this design 
  feedback: Layout is too cramped...
2025-12-16 20:54:42 - LLM Response: 324 characters
2025-12-16 20:54:42 - Kroki Validation: SUCCESS
2025-12-16 20:54:42 - Iteration 2/10 - COMPLETE (design improvement)
```

**3. Technische Lösung**

- **Python logging Module**: Standard, strukturiert, mit FileHandler für Log-Datei
- **Konsole**: Direktes `click.echo()` für minimalen Progress
- **Log-Level**: INFO für normale Ausgabe, DEBUG für sehr detaillierte Infos
- **Log-Format**: Timestamp + Level + Message

## Notes

### Aktueller Code-Stand

**CLI (src/diag_agent/cli/commands.py)**:
- `create()` Funktion (Lines 26-75) zeigt nur Endergebnis:
  ```python
  result = orchestrator.execute(...)
  click.echo(f"✓ Diagram generated: {result['output_path']}")
  click.echo(f"  Iterations: {result['iterations_used']}")
  # etc.
  ```
- Keine Progress-Updates während der Ausführung

**Orchestrator (src/diag_agent/agent/orchestrator.py)**:
- `execute()` Methode (Lines 95-227) hat While-Loop für Iterationen
- Interne Variablen: `validation_error`, `design_feedback`
- Drei Prompt-Typen:
  1. Initial: "Generate a {diagram_type} diagram: {description}"
  2. Syntax-Fix: "Fix the following... error: {validation_error}"
  3. Design-Improvement: "Improve... feedback: {design_feedback}"
- Keine Ausgaben während der Iteration

### Mögliche Lösungen

1. **Python logging Module** (Standard-Lösung):
   - Pro: Standard-Library, konfigurierbar, verschiedene Levels
   - Contra: Muss konfiguriert werden
   
2. **Callback-System**:
   - Pro: Flexibel, testbar, Separation of Concerns
   - Contra: Etwas komplexer

3. **Direktes click.echo()** (Einfachste Lösung):
   - Pro: Einfach, funktioniert sofort
   - Contra: Schwerer testbar, tight coupling

4. **Event-System** (Observer Pattern):
   - Pro: Sehr flexibel, erweiterbar
   - Contra: Overkill für diesen Use-Case

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
