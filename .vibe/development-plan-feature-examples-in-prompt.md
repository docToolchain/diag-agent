# Development Plan: diag-agent (feature/examples-in-prompt branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Beispiel-basierte LLM-Prompts: LLM soll passende Beispiele als Referenz bekommen für bessere Diagramm-Generierung

**Problem**: 
Aktuell generiert das LLM "blind" ohne Beispiele → oft suboptimale Syntax und Layout

**Lösung - Drei Komponenten**:
1. **Subtype Detection**: LLM analysiert description und bestimmt Subtype (sequence, context, flowchart, etc.)
2. **Beispiel-Loader**: Lädt passendes Beispiel aus `examples/{diagram_type}/{subtype}*`
3. **Prompt Enhancement**: Fügt Beispiel zum LLM-Prompt hinzu als Referenz

**Scope**:
- Mechanik mit vorhandenen Beispielen (bpmn, c4plantuml)
- Keine neuen Beispiele erstellen (separate Task)
- --type Parameter überschreibt Auto-Detection (bleibt optional)

## Explore
### Tasks
*All exploration completed*

### Completed
- [x] Plan erstellt
- [x] Beispiel-Struktur analysiert
  - bpmn: simple-process, collaboration
  - c4plantuml: context-diagram, container-diagram, component-diagram
  - Naming: {subtype}.{ext} oder {subtype}-diagram.{ext}
- [x] Orchestrator.execute() analysiert
  - 3 Prompt-Typen: initial (line 202), syntax fix (line 190), design refinement (line 197)
  - diagram_type bekannt, description verfügbar
- [x] Beispiel-Loader-Design: PathLib-basiert, Fallback auf erstes Beispiel
- [x] Subtype-Detection-Strategie: LLM-Call VOR Loop
- [x] Prompt-Enhancement-Strategie: "\n\nExample:\n{example_content}" anhängen

### Completed
- [x] Created development plan file

## Red

### Phase Entrance Criteria:
- [x] Subtype-Detection-Strategie ist klar definiert
- [x] Beispiel-Loader-Design ist dokumentiert
- [x] Prompt-Enhancement-Strategie ist definiert
- [x] Integration-Points identifiziert (wo Code geändert wird)
- [x] Test-Strategie ist klar

### Tasks
*All tests written and validated*

### Completed
- [x] Test 1-3: _detect_subtype() Unit Tests (context, container, simple-process)
- [x] Test 4-7: _load_example() Unit Tests (exact match, fallback, none)
- [x] Test 8: Integration Test - Beispiel im Initial Prompt
- [x] Test 9: Integration Test - Backward Compatibility (ohne Beispiele)
- [x] Alle Tests ausgeführt - 8 failed, 1 passed (wie erwartet) ✅

## Green

### Phase Entrance Criteria:
- [ ] Tests sind geschrieben und schlagen erwartungsgemäß fehl
- [ ] Test-Failures zeigen die fehlende Funktionalität klar auf
- [ ] Alle Tests wurden ausgeführt und validiert

### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Refactor

### Phase Entrance Criteria:
- [ ] Implementierung ist abgeschlossen
- [ ] Alle Tests sind grün
- [ ] Funktionalität ist vollständig und korrekt

### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Key Decisions

### EXPLORE Phase

**1. Drei-Komponenten-Architektur**

**Komponente 1: Subtype Detection**
- **Wann**: VOR dem Iterations-Loop (nur einmal)
- **Input**: `description` + `diagram_type`
- **Output**: `subtype` (z.B. "context", "sequence", "flowchart")
- **Methode**: Neuer LLM-Call mit kurzem Prompt
- **Beispiel-Prompt**: "What subtype of {diagram_type} diagram best fits: '{description}'? Respond with just the subtype name (e.g., 'context', 'sequence', 'activity')."

**Komponente 2: Beispiel-Loader**
- **Location**: Neue Methode `_load_example(diagram_type, subtype)` in Orchestrator
- **Suchstrategie**:
  1. Exaktes Match: `examples/{diagram_type}/{subtype}*`
  2. Fallback: Erstes verfügbares Beispiel in `examples/{diagram_type}/`
  3. None: Wenn kein Beispiel verfügbar
- **Return**: `Optional[str]` (Beispiel-Content oder None)

**Komponente 3: Prompt Enhancement**
- **Where**: In allen 3 Prompt-Typen (initial, syntax fix, design refinement)
- **Format**: 
  ```
  {original_prompt}
  
  Example {diagram_type} diagram for reference:
  {example_content}
  ```
- **Conditional**: Nur wenn example_content verfügbar

**2. Integration-Points**

- **orchestrator.py line 126**: `execute()` - Subtype Detection + Beispiel laden VOR Loop
- **orchestrator.py lines 190, 197, 202**: Prompt-Konstruktion - Example anhängen
- **Neue Methode**: `_load_example(diagram_type: str, subtype: str) -> Optional[str]`
- **Neue Methode**: `_detect_subtype(description: str, diagram_type: str) -> str`

**3. Scope-Decisions**

✅ **IN Scope**:
- Subtype Detection via LLM
- Beispiel-Loader mit Fallback
- Prompt Enhancement in allen 3 Prompt-Typen
- Integration mit vorhandenen Beispielen (bpmn, c4plantuml)

❌ **OUT of Scope** (separate Tasks):
- Neue Beispiele erstellen (PlantUML sequence, Mermaid flowchart, etc.)
- Beispiel-Caching
- Multi-Beispiel-Strategie (mehrere Beispiele kombinieren)
- Auto-Detection von diagram_type (nur subtype)

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
