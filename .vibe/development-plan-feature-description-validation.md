# Development Plan: diag-agent (feature/description-validation branch)

*Generated on 2025-12-17 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Implementierung einer LLM-gestützten Validierung der Diagramm-Beschreibung vor der Generierung.

**Problem**: Aktuell werden ungenaue, inkonsistente oder unvollständige Beschreibungen ohne Prüfung akzeptiert, was zu suboptimalen Diagrammen führt.

**Lösung**: Das LLM soll die Beschreibung analysieren und bei Problemen interaktiv nachfragen. Ein `--force` Flag soll die Validierung überspringen können.

**GitHub Issue**: #1

## Requirements

### Funktionale Anforderungen
1. **Beschreibungs-Analyse durch LLM**
   - Prüfung auf Vollständigkeit (fehlen wichtige Informationen?)
   - Prüfung auf Konsistenz (gibt es Widersprüche?)
   - Prüfung auf Klarheit (ist die Beschreibung eindeutig?)
   - Berücksichtigung des Diagramm-Typs bei der Analyse

2. **Interaktive Rückfrage**
   - Bei Problemen: Ausgabe der Fragen/Unklarheiten über stdout
   - Klare, nummerierte Fragen
   - Aufforderung, das Tool mit verbesserter Beschreibung nochmal aufzurufen
   - Exit-Code 1 bei abgebrochenem Prozess

3. **Force-Parameter**
   - CLI-Flag `--force` oder `-f`
   - Überspringt die Validierung komplett
   - Für automatisierte Workflows und bewusste Nutzung mit unvollständiger Beschreibung

### Nicht-Funktionale Anforderungen
- Keine zusätzliche Verzögerung bei `--force`
- Schnelle Validierung (< 5 Sekunden)
- Klare, benutzerfreundliche Ausgabe
- Logging der Validierungs-Entscheidung

### Edge Cases
1. **Sehr kurze Beschreibungen**: "BPMN diagram" → zu unspezifisch
2. **Sehr lange Beschreibungen**: Mehrere Absätze → könnte OK sein
3. **Widersprüchliche Angaben**: "3 Akteure" aber nur 2 genannt
4. **Fehlender Kontext**: "Update the existing diagram" → welches?
5. **Force-Flag Nutzung**: Validierung komplett überspringen
6. **Automatisierte Workflows**: Muss mit `--force` funktionieren
7. **API-Key Fehler**: Was passiert wenn LLM nicht erreichbar?

## Explore
### Tasks
- [x] Verstehen der Orchestrator-Struktur
- [x] Verstehen der LLM-Client-Integration
- [x] Verstehen der CLI-Parameter-Übergabe
- [x] Ähnliche Validierungsmuster im Codebase finden
- [x] Requirements für Beschreibungs-Validierung dokumentiert
- [x] Edge Cases dokumentiert
- [x] Detailliertes Requirements-Dokument erstellt

### Completed
- [x] Created development plan file
- [x] Orchestrator.execute() analysiert (orchestrator.py:211-401)
- [x] LLMClient-Struktur verstanden (generate, vision_analyze methods)
- [x] CLI create-Command verstanden (commands.py:26-89)

## Plan

### Phase Entrance Criteria:
- [x] Existing code structure understood (orchestrator, LLM client, CLI)
- [x] Similar validation patterns in codebase identified
- [x] Requirements for description validation clarified
- [x] Edge cases and user workflows documented

### Implementation Strategy

#### 1. LLM Prompt Design für Beschreibungs-Validierung
**Ziel**: Prompt entwickeln, der Beschreibungen präzise validiert

**Ansatz**:
```
System: You are a diagram description validator. Analyze the given description for a {diagram_type} diagram.

Check for:
1. Completeness: Are essential elements specified?
2. Consistency: Are there contradictions?
3. Clarity: Is the description unambiguous?

Response format:
- If valid: Return "VALID"
- If invalid: Return "INVALID" followed by numbered questions on separate lines

Example:
INVALID
1. Which type of BPMN diagram? (process/collaboration/choreography)
2. Who performs the "approval step"? (role/system)
```

**Design-Entscheidungen**:
- Maschinenlesbares Format (VALID/INVALID Präfix)
- Nummerierte Fragen für Parsing
- Diagramm-Typ-spezifische Validierung
- Keine Erklärungen, nur konkrete Fragen

#### 2. LLMClient Erweiterung
**Neue Methode**: `validate_description(description: str, diagram_type: str) -> tuple[bool, Optional[str]]`

**Returns**:
- `(True, None)`: Beschreibung ist valide
- `(False, "questions")`: Beschreibung invalide, questions enthält Rückfragen

**Exception Handling**:
- Bei LLM-API-Fehler: Log warning, return `(True, None)` (fortfahren wie mit --force)
- Robust gegen Parsing-Fehler

#### 3. CLI Integration
**Änderungen in `commands.py`**:
- Neuer Parameter: `@click.option("--force", "-f", is_flag=True, help="Skip description validation")`
- Parameter an `Orchestrator.execute()` übergeben

#### 4. Orchestrator Integration
**Änderungen in `orchestrator.py`**:
- Neuer Parameter in `execute()`: `skip_validation: bool = False`
- Validierung nach Zeile 248 (nach Example Loading)
- Bei INVALID: Ausgabe der Fragen + Exit mit Code 1
- Bei --force oder Validierungs-Fehler: Überspringen mit Log-Meldung

**Flow**:
```python
# Nach Example Loading (Zeile 248)
if not skip_validation:
    is_valid, questions = self.llm_client.validate_description(description, diagram_type)
    if not is_valid:
        # Print questions to stderr (visible to user)
        click.echo("\n❌ Die Beschreibung enthält Unklarheiten:\n", err=True)
        click.echo(questions, err=True)
        click.echo("\nBitte rufe das Tool mit einer präziseren Beschreibung erneut auf.", err=True)
        click.echo("Oder nutze --force um diese Validierung zu überspringen.\n", err=True)
        sys.exit(1)
    logger.info("Description validation: PASSED")
else:
    logger.info("Description validation: SKIPPED (--force)")
```

#### 5. Test-Strategie

**Unit Tests**:
- `test_llm_client.py`: 
  - `test_validate_description_valid()`
  - `test_validate_description_invalid_with_questions()`
  - `test_validate_description_api_error_fallback()`
  - `test_validate_description_parsing_error_fallback()`

- `test_orchestrator.py`:
  - `test_orchestrator_validates_description_before_generation()`
  - `test_orchestrator_skips_validation_with_force_flag()`
  - `test_orchestrator_exits_on_invalid_description()`

- `test_cli.py`:
  - `test_create_command_with_force_flag()`
  - `test_create_command_validation_failure_exits()`

**Integration Tests**:
- `test_orchestrator_integration.py`:
  - `test_description_validation_integration()`
  - Full workflow test mit Mock-LLM

### Tasks
- [x] Prompt Design ausgearbeitet
- [x] API-Signatur für validate_description() definiert
- [x] CLI-Integration geplant
- [x] Orchestrator-Integration geplant
- [x] Test-Strategie definiert
- [x] Fehlerbehandlung spezifiziert

### Completed
- [x] Detaillierter Implementierungsplan erstellt
- [x] Alle Komponenten durchdacht
- [x] Edge Cases berücksichtigt

## Code

### Phase Entrance Criteria:
- [ ] Implementation plan is complete and approved
- [ ] Technical approach decided (LLM prompt design, CLI integration)
- [ ] Test strategy defined
- [ ] Impact on existing code assessed

### Tasks

#### LLM Client Erweiterung
- [x] `validate_description()` Methode in `llm/client.py` implementieren
- [x] Prompt Design umsetzen mit VALID/INVALID Parsing
- [x] Exception Handling für API-Fehler (fallback zu True, None)
- [x] Bestehende Tests angepasst (validate_description mocken)

#### CLI Integration
- [x] `--force` / `-f` Flag zu `create` Command hinzufügen
- [x] Flag an Orchestrator.execute() durchreichen
- [ ] CLI Tests für --force Flag schreiben

#### Orchestrator Integration
- [x] `skip_validation` Parameter zu execute() hinzufügen
- [x] Validierung nach Example Loading einfügen (nach Zeile 248)
- [x] Ausgabe-Logik für INVALID-Fall implementieren (stderr)
- [x] Logging für PASSED/SKIPPED hinzufügen
- [x] Exit-Code 1 bei INVALID ohne --force
- [ ] Unit Tests für Validierungs-Flow schreiben

#### Integration Tests
- [ ] End-to-End Test mit Mock-LLM
- [ ] Test für --force Flag Workflow
- [ ] Test für Validierungs-Fehler-Fallback

#### Dokumentation
- [ ] CLI Help Text aktualisieren
- [ ] Logging-Meldungen dokumentieren

### Completed
*None yet*

## Commit

### Phase Entrance Criteria:
- [ ] Feature implementation complete and working
- [ ] All tests passing (unit + integration)
- [ ] End-to-end testing successful
- [ ] Documentation updated

### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Key Decisions

### Validierungs-Strenge
**Entscheidung**: Nicht zu streng - nur bei echten Problemen (fehlende/inkonsistente Informationen)

**Rationale**: 
- Fokus auf tatsächliche Probleme, die zu schlechten Diagrammen führen
- Nicht jede kleine Ungenauigkeit sollte Rückfragen auslösen
- User Experience: Nicht zu viele Unterbrechungen

### Zielgruppe der Rückfragen
**Entscheidung**: Professionell, Zielgruppe ist das aufrufende LLM (nicht Endnutzer)

**Rationale**:
- Das Tool wird oft von anderen LLMs aufgerufen
- Präzise, strukturierte Rückmeldungen sind wichtiger als umgangssprachliche Erklärungen
- Format muss maschinenlesbar und eindeutig sein

### Fehlerbehandlung bei Validierungs-Problemen
**Entscheidung**: Bei API-Fehler oder Validierungs-Fehler mit Warning fortfahren (wie --force)

**Rationale**:
- Robustheit wichtiger als Perfektion
- Validierung ist ein "Nice-to-have", nicht kritisch
- Kein Totalausfall wenn Validierungs-LLM nicht erreichbar
- Warning loggen für Debugging

## Notes

### Code-Struktur Erkenntnisse

**Orchestrator Flow** (orchestrator.py):
1. Subtype Detection (Zeile ~246-247)
2. Example Loading (Zeile ~248)
3. **→ HIER: Beschreibungs-Validierung einfügen**
4. Iterations-Loop beginnt (Zeile ~260)
5. LLM-Generierung → Kroki-Validierung → Design-Validierung

**LLM-Client** (llm/client.py):
- `generate()`: Text-Generierung
- `vision_analyze()`: Bild-Analyse
- **→ NEU: `validate_description()` Method hinzufügen**

**CLI Integration** (cli/commands.py):
- `create()` Command nimmt Parameter entgegen
- **→ NEU: `--force` / `-f` Flag hinzufügen**
- Orchestrator.execute() wird aufgerufen

### Bestehende Validierungsmuster
- **Kroki-Validierung**: Syntaktische Validierung durch Rendering (orchestrator.py:303-354)
- **Design-Validierung**: Optional durch Vision-LLM (orchestrator.py:315-345)
- Beide laufen NACH der Generierung im Loop

### Unterschied zur neuen Validierung
- Läuft VOR der Generierung
- Validiert INPUT (Beschreibung) statt OUTPUT (Diagramm)
- Interaktive Rückfrage statt automatischer Retry

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
